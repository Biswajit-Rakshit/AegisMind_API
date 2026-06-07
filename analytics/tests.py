from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Department

User = get_user_model()

class AnalyticsAPITests(APITestCase):
    '''Test case for analytics API endpoints'''

    def setUp(self):
        '''Set up test data for analytics API tests'''

        self.eng_department = Department.objects.create(name='Engineering')
        self.sales_department = Department.objects.create(name='Sales')
        self.employee1 = User.objects.create_user(
            username='employee1',
            email='employee1@example.com',
            department=self.eng_department,
            password='employeepassword'
        )
        self.employee2 = User.objects.create_user(
            username='employee2',
            email='employee2@example.com',
            department=self.eng_department,
            password='employeepassword'
        )
        self.employee3 = User.objects.create_user(
            username='employee3',
            email='employee3@example.com',
            department=self.eng_department,
            password='employeepassword'
        )
        self.employee4 = User.objects.create_user(
            username='employee4',
            email='employee4@example.com',
            department=self.eng_department,
            password='employeepassword'
        )
        self.employee5 = User.objects.create_user(
            username='employee5',
            email='employee5@example.com',
            department=self.eng_department,
            password='employeepassword'
        )
        self.employee6 = User.objects.create_user(
            username='employee6',
            email='employee6@example.com',
            department=self.sales_department,
            password='employeepassword'
        )
        self.hr_user = User.objects.create_user(
            username='hruser',
            email='hruser@example.com',
            department=self.eng_department,
            password='hrpassword',
            role = 'hr'
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            email='adminuser@example.com',
            department=self.eng_department,
            password='adminpassword'
        )
        self.user_tokens = {
            'employee1': str(RefreshToken.for_user(self.employee1).access_token),
            'employee2': str(RefreshToken.for_user(self.employee2).access_token),
            'employee3': str(RefreshToken.for_user(self.employee3).access_token),
            'employee4': str(RefreshToken.for_user(self.employee4).access_token),
            'employee5': str(RefreshToken.for_user(self.employee5).access_token),
            'employee6': str(RefreshToken.for_user(self.employee6).access_token),
            'hr_user': str(RefreshToken.for_user(self.hr_user).access_token),
            'admin_user': str(RefreshToken.for_user(self.admin_user).access_token)
        }
        

        for employee in [self.employee1, self.employee2, self.employee3, self.employee4, self.employee5, self.employee6]:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_tokens[employee.username])
            survey_response_data = {
            'user_id': employee.id,
            'department_id': employee.department.id,
            'stress_score': 5,
            'workload_score': 6,
            'mood_score': 7,
            'burnout_score': 4
        }
            self.client.post(reverse('survey-submit'), survey_response_data, format='json')

    def test_get_department_analytics_hr_user(self):
        '''Test that HR user can access department analytics data'''

        url = reverse('department-analytics', args=[self.eng_department.name])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_tokens['hr_user'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('avg_stress_score', response.data)
        self.assertIn('avg_workload_score', response.data)
        self.assertIn('avg_mood_score', response.data)
        self.assertIn('avg_burnout_score', response.data)

    def test_get_department_analytics_employee_user(self):
        '''Test that employee user cannot access department analytics data'''

        url = reverse('department-analytics', args=[self.eng_department.name])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_tokens['employee1'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_department_analytics_admin_user(self):
        '''Test that admin user cannot access department analytics data'''

        url = reverse('department-analytics', args=[self.eng_department.name])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_tokens['admin_user'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_department_analytics_not_enough_data(self):
        '''Test that department analytics endpoint returns 403 if there is not enough data'''

        url = reverse('department-analytics', args=[self.sales_department.name])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_tokens['hr_user'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Not enough data for analytics")

    def test_get_overall_analytics_hr_user(self):
        '''Test that HR user can access overall analytics data'''

        url = reverse('overall-analytics')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_tokens['hr_user'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        
    def test_get_overall_analytics_employee_user(self):
        '''Test that employee user cannot access overall analytics data'''

        url = reverse('overall-analytics')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_tokens['employee1'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_overall_analytics_admin_user(self):
        '''Test that admin user cannot access overall analytics data'''

        url = reverse('overall-analytics')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_tokens['admin_user'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)