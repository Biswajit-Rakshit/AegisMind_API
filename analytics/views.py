from django.shortcuts import render
from rest_framework.views import APIView, Response
from django.db.models import Avg, Count
from rest_framework import status
from django.db import models

from surveys.models import SurveyResponse
from accounts.models import Department

class DepartmentAnalyticsAPIView(APIView):
    '''API view for analytics data'''

    def get(self, request, department_name):
        '''Handle GET request for analytics data'''

        departments = Department.objects.all()

        if not departments.filter(name__iexact=department_name).exists():
            return Response({"detail": "Department not found"}, status=status.HTTP_404_NOT_FOUND)

        queryset = SurveyResponse.objects.filter(department_id__name__iexact=department_name)

        if queryset.count() < 5:
            return Response({"detail": "Not enough data for analytics"}, status=status.HTTP_403_FORBIDDEN)
        
        data = queryset.aggregate(
            avg_stress_score=Avg('stress_score'),
            avg_workload_score=Avg('workload_score'),
            avg_mood_score=Avg('mood_score'),
            avg_burnout_score=Avg('burnout_score'),
        )  

        return Response(data, status=status.HTTP_200_OK)
    
class OverallAnalyticsAPIView(APIView):
    '''API view for overall analytics data'''

    def get(self, request):

        analytics = SurveyResponse.objects.values(
            departments=models.F('department_id__name')).annotate(
            response_count=Count('id'),
            avg_stress=Avg('stress_score'),
            avg_workload=Avg('workload_score'),
            avg_mood=Avg('mood_score'),
            avg_burnout=Avg('burnout_score')
        ).filter(response_count__gte=5)

        return Response(list(analytics))

