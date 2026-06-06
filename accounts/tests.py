from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserAPITests(APITestCase):
    def setUp(self):
        '''Set up test data for user API tests'''

        self.user = User.objects.create_user(username='testuser',email='testuser@example.com', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser',email='adminuser@example.com', password='adminpassword')
        self.user_token = str(RefreshToken.for_user(self.user).access_token)
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)

    def test_user_list_unauthenticated(self):
        '''Test that unauthenticated users cannot access the user list'''

        url = reverse('user-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_authenticated_non_admin(self):
        '''Test that authenticated non-admin users cannot access the user list'''

        url = reverse('user-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_list_authenticated_admin(self):
        '''Test that authenticated admin users can access the user list'''

        url = reverse('user-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_user_create_unauthenticated(self):
        '''Test that unauthenticated users cannot create a user'''

        url = reverse('user-list-create')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create_authenticated_non_admin(self):
        '''Test that authenticated non-admin users cannot create a user'''

        url = reverse('user-list-create')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_create_authenticated_admin(self):
        '''Test that authenticated admin users can create a user'''

        url = reverse('user-list-create')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_user_detail_unauthenticated(self):
        '''Test that unauthenticated users cannot access user details'''

        url = reverse('user-detail', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_detail_authenticated_non_admin(self):
        '''Test that authenticated non-admin users cannot access user details'''

        url = reverse('user-detail', kwargs={'username': self.user.username})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_detail_authenticated_admin(self):
        '''Test that authenticated admin users can access user details'''

        url = reverse('user-detail', kwargs={'username': self.user.username})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)