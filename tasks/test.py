from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.cache import cache
from django.contrib.auth import get_user_model

class RateLimitTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            email='user@example.com'
        )
        self.url = '/api/rate-limited/'

    def test_rate_limit(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Ensure cache is clear before testing
        cache.clear()

        # Perform 5 successful requests (within limit)
        for _ in range(5):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 6th request should be rate-limited
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertEqual(response.data['message'], "Rate limit exceeded. Try again later.")

    def tearDown(self):
        cache.clear()