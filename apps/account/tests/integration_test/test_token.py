import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase

from apps.account.tests.factories import UserFactory, PASSWORD


class TokenTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(is_staff=False)
        cls.staff = UserFactory(is_staff=True)
        cls.url = '/api/v1/account/token/'

    def test_jwt_token_payload(self):
        response = self.client.post(self.url, {'username': self.user.username, 'password': PASSWORD})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['refresh']
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.SIMPLE_JWT['ALGORITHM'])
        keys = payload.keys()
        self.assertIn('full_name', keys)
        self.assertIn('is_staff', keys)
        self.assertFalse(payload['is_staff'])

    def test_is_staff(self):
        token = self.client.post(self.url, {'username': self.staff.username, 'password': PASSWORD}).data['refresh']
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.SIMPLE_JWT['ALGORITHM'])
        self.assertTrue(payload['is_staff'])
        self.assertEqual(payload['full_name'], self.staff.get_full_name())
