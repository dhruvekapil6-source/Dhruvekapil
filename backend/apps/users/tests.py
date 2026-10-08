from urllib.parse import parse_qs, urlparse

from django.contrib.auth.models import User
from django.core import mail
from django.test import override_settings
from rest_framework.test import APITestCase

from .models import UserProfile


class UserSecurityTests(APITestCase):
    def test_login_returns_access_and_refresh_tokens(self):
        User.objects.create_user(username='fleet-user', password='StrongPass123!')

        response = self.client.post(
            '/api/token/',
            {'username': 'fleet-user', 'password': 'StrongPass123!'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_registration_cannot_assign_privileged_role(self):
        response = self.client.post(
            '/api/users/register/',
            {
                'username': 'new-customer',
                'email': 'customer@example.com',
                'password': 'StrongPass123!',
                'role': 'admin',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        profile = UserProfile.objects.get(user__username='new-customer')
        self.assertEqual(profile.role, 'customer')

    def test_users_can_only_list_their_own_account(self):
        user = User.objects.create_user(username='customer', password='StrongPass123!')
        UserProfile.objects.create(user=user, role='customer')
        other_user = User.objects.create_user(username='other', password='StrongPass123!')
        UserProfile.objects.create(user=other_user, role='customer')
        self.client.force_authenticate(user=user)

        response = self.client.get('/api/users/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item['username'] for item in response.data['results']], ['customer'])

    def test_users_cannot_promote_their_own_profile(self):
        user = User.objects.create_user(username='customer', password='StrongPass123!')
        profile = UserProfile.objects.create(user=user, role='customer')
        self.client.force_authenticate(user=user)

        response = self.client.patch(
            f'/api/users/profiles/{profile.pk}/',
            {'role': 'admin', 'is_active': False},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        profile.refresh_from_db()
        self.assertEqual(profile.role, 'customer')
        self.assertTrue(profile.is_active)

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        DEFAULT_FROM_EMAIL='noreply@example.com',
        FRONTEND_URL='http://testserver',
    )
    def test_password_reset_request_emails_link_without_returning_credentials(self):
        user = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='StrongPass123!',
        )
        UserProfile.objects.create(user=user, role='customer')

        response = self.client.post(
            '/api/users/password-reset/request/',
            {'identifier': 'customer@example.com'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('uid', response.data)
        self.assertNotIn('reset_token', response.data)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('/pages/forgot-password.html?uid=', mail.outbox[0].body)

        reset_url = mail.outbox[0].body.strip().splitlines()[-1]
        credentials = parse_qs(urlparse(reset_url).query)
        confirm_response = self.client.post(
            '/api/users/password-reset/confirm/',
            {
                'uid': credentials['uid'][0],
                'token': credentials['token'][0],
                'new_password': 'NewStrongPass123!',
            },
            format='json',
        )

        self.assertEqual(confirm_response.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.check_password('NewStrongPass123!'))

    def test_non_admin_cannot_view_audit_logs(self):
        user = User.objects.create_user(username='customer', password='StrongPass123!')
        UserProfile.objects.create(user=user, role='customer')
        self.client.force_authenticate(user=user)

        response = self.client.get('/api/users/audit-logs/')

        self.assertEqual(response.status_code, 403)