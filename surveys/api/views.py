from django.shortcuts import render
from rest_framework import generics

from surveys.api.throttling import OncePerCalendarWeekThrottle
from surveys.models import SurveyResponse
from surveys.api.serializers import SurveyResponseSerializer
from accounts.api.permissions import IsEmployee

class SurveyResponseCreateView(generics.CreateAPIView):
    '''APIView for creating survey responses'''

    throttle_classes = [OncePerCalendarWeekThrottle]

    permission_classes = [IsEmployee]

    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer
    
    def perform_create(self, serializer):
        '''Override perform_create to set user and department based on the authenticated user'''

        user_id = self.request.user
        department_id = self.request.user.department
        serializer.save(user_id=user_id, department_id=department_id)