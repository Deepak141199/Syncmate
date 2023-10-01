from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

class UserProfileViewTestCase(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Obtain an authentication token for the user
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_user_profile_view(self):
        # Set the authentication token in the request headers
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Make a GET request to the profile endpoint
        response = self.client.get('/api/profile/')

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)




class CustomAuthTokenTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_custom_auth_token(self):
        # Make a POST request to the custom auth token endpoint with valid credentials
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'testpassword'
        })
        
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)













