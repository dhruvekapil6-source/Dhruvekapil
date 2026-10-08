from django.contrib.auth.models import User
from django.urls import resolve
from django.views.generic import TemplateView
from django.test import SimpleTestCase
from rest_framework.test import APITestCase

from apps.users.models import UserProfile


class FleetPageRouteTests(SimpleTestCase):
    def test_dashboard_sidebar_destinations_resolve(self):
        pages = (
            'dashboard.html',
            'vehicles.html',
            'drivers.html',
            'trips.html',
            'routes.html',
            'fuel.html',
            'maintenance.html',
            'reports.html',
            'notifications.html',
            'profile.html',
            'trip-details.html',
        )

        for page in pages:
            with self.subTest(page=page):
                view = resolve(f'/pages/{page}').func
                self.assertIs(view.view_class, TemplateView)


class FleetRoleAccessTests(APITestCase):
    def test_customer_cannot_access_fleet_management_apis(self):
        user = User.objects.create_user(username='customer', password='StrongPass123!')
        UserProfile.objects.create(user=user, role='customer')
        self.client.force_authenticate(user=user)
        endpoints = (
            '/api/dashboard/',
            '/api/vehicles/',
            '/api/drivers/',
            '/api/trips/',
            '/api/routes/',
            '/api/fuel/entries/',
            '/api/maintenance/records/',
            '/api/reports/',
            '/api/notifications/',
        )

        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                self.assertEqual(self.client.get(endpoint).status_code, 403)

    def test_fleet_manager_can_access_dashboard_and_vehicle_api(self):
        user = User.objects.create_user(username='fleet-manager', password='StrongPass123!')
        UserProfile.objects.create(user=user, role='fleet_manager')
        self.client.force_authenticate(user=user)

        self.assertEqual(self.client.get('/api/dashboard/').status_code, 200)
        self.assertEqual(self.client.get('/api/vehicles/').status_code, 200)

    def test_user_without_profile_is_denied_but_staff_user_is_allowed(self):
        user = User.objects.create_user(username='unprofiled-user', password='StrongPass123!')
        self.client.force_authenticate(user=user)
        self.assertEqual(self.client.get('/api/dashboard/').status_code, 403)

        staff_user = User.objects.create_user(
            username='staff-user',
            password='StrongPass123!',
            is_staff=True,
        )
        self.client.force_authenticate(user=staff_user)
        self.assertEqual(self.client.get('/api/dashboard/').status_code, 200)