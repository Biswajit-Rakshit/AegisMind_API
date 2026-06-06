from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Department

User = get_user_model()

class SurveyResponseAPITests(APITestCase):
    '''Test case for survey response API endpoints'''

    def setUp(self):
        '''Set up test data for survey response API tests'''

        self.department = Department.objects.create(name='Engineering')
        self.employee = User.objects.create_user(
            username='employee',
            email='employee@example.com',
            password='employeepassword',
            department=self.department,
            role = 'employee'
        )
        self.hr_user = User.objects.create_user(
            username='hruser',
            email='hruser@example.com',
            password='hrpassword',
            department=self.department,
            role = 'hr'
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            email='adminuser@example.com',
            password='adminpassword',
            department=self.department
        )
        self.survey_response_data = {
            'user_id': self.employee.id,
            'department_id': self.department.id,
            'stress_score': 5,
            'workload_score': 6,
            'mood_score': 7,
            'burnout_score': 4
        }
        self.survey_response_data_invalid = {
            'user_id': self.employee.id,
            'department_id': self.department.id,
            'stress_score': 15,
            'workload_score': 0,
            'mood_score': -4,
            'burnout_score': 11
        }
        self.user_tokens = {
            'employee': str(RefreshToken.for_user(self.employee).access_token),
            'hr_user': str(RefreshToken.for_user(self.hr_user).access_token),
            'admin_user': str(RefreshToken.for_user(self.admin_user).access_token)
        }

        url = reverse('survey-submit')

    def test_get_request_not_allowed_unauthorized(self):
        '''Test that GET request to survey response endpoint is not allowed for unauthorized users'''

        url = reverse('survey-submit')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_request_not_allowed_employee(self):
        '''Test that GET request to survey response endpoint is not allowed for employee users'''

        url = reverse('survey-submit')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_tokens['employee'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_request_not_allowed_hr_user(self):
        '''Test that GET request to survey response endpoint is not allowed for HR users'''

        url = reverse('survey-submit')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_tokens['hr_user'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_request_not_allowed_admin_user(self):
        '''Test that GET request to survey response endpoint is not allowed for admin users'''

        url = reverse('survey-submit')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_tokens['admin_user'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_request_create_survey_response_employee(self):
        '''Test that POST request to create survey response is successful for employee users'''

        url = reverse('survey-submit')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_tokens['employee'])
        response = self.client.post(url, self.survey_response_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user_id'], self.survey_response_data['user_id'])
        self.assertEqual(response.data['department_id'], self.survey_response_data['department_id'])
        self.assertEqual(response.data['stress_score'], self.survey_response_data['stress_score'])
        self.assertEqual(response.data['workload_score'], self.survey_response_data['workload_score'])
        self.assertEqual(response.data['mood_score'], self.survey_response_data['mood_score'])
        self.assertEqual(response.data['burnout_score'], self.survey_response_data['burnout_score'])

    def test_post_request_create_survey_response_invalid_data(self):
        '''Test that POST request to create survey response with invalid data is not successful'''

        url = reverse('survey-submit')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_tokens['employee'])
        response = self.client.post(url, self.survey_response_data_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('stress_score', response.data)
        self.assertIn('workload_score', response.data)
        self.assertIn('mood_score', response.data)
        self.assertIn('burnout_score', response.data)

    def test_post_request_create_survey_response_hr_user(self):
        '''Test that POST request to create survey response is not allowed for HR users'''

        url = reverse('survey-submit')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_tokens['hr_user'])
        response = self.client.post(url, self.survey_response_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_request_create_survey_response_admin_user(self):
        '''Test that POST request to create survey response is not allowed for admin users'''

        url = reverse('survey-submit')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_tokens['admin_user'])
        response = self.client.post(url, self.survey_response_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)