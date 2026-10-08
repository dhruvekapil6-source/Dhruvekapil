from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from apps.users.models import UserProfile


class VehicleApiTests(APITestCase):
    def test_authenticated_user_can_create_and_list_vehicles(self):
        user = User.objects.create_user(username='fleet-user', password='StrongPass123!')
        UserProfile.objects.create(user=user, role='fleet_manager')
        self.client.force_authenticate(user=user)

        create_response = self.client.post(
            '/api/vehicles/',
            {
                'vehicle_number': 'TRK-001',
                'vehicle_type': 'Truck',
                'registration_number': 'REG-001',
                'purchase_date': '2024-01-01',
            },
            format='json',
        )

        self.assertEqual(create_response.status_code, 201)
        list_response = self.client.get('/api/vehicles/')
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.data['count'], 1)
        self.assertEqual(list_response.data['results'][0]['vehicle_number'], 'TRK-001')

        update_response = self.client.patch(
            f"/api/vehicles/{create_response.data['id']}/",
            {'status': 'maintenance', 'current_location': 'Central depot', 'total_distance': 1234.5},
            format='json',
        )

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data['status'], 'maintenance')
        self.assertEqual(update_response.data['current_location'], 'Central depot')
        self.assertEqual(update_response.data['total_distance'], 1234.5)

    def test_vehicle_api_requires_authentication(self):
        response = self.client.get('/api/vehicles/')

        self.assertEqual(response.status_code, 401)