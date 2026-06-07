from django.shortcuts import render
from rest_framework.views import APIView, Response
from django.db.models import Avg, Count
from rest_framework import status
from django.db import models
from drf_spectacular.utils import extend_schema, OpenApiResponse

from analytics.api.service import get_analytics, get_department_analytics
from surveys.models import SurveyResponse
from accounts.models import Department
from accounts.api.permissions import IsHR
from analytics.api.serializers import DepartmentAnalyticsResponseSerializer, OverallAnalyticsResponseSerializer

class DepartmentAnalyticsAPIView(APIView):
    '''API view for analytics data'''

    permission_classes = [IsHR]

    @extend_schema(
        description="Retrieves aggregated survey scores for a specific department. Requires a minimum of 5 responses for privacy.",
        responses={
            200: DepartmentAnalyticsResponseSerializer,
            403: OpenApiResponse(description="Not enough data for analytics (less than 5 responses)."),
            404: OpenApiResponse(description="Department not found.")
        }
    )

    def get(self, request, department_name):
        '''Handle GET request for analytics data'''

        departments = Department.objects.all()

        if not departments.filter(name__iexact=department_name).exists():
            return Response({"detail": "Department not found"}, status=status.HTTP_404_NOT_FOUND)

        queryset = SurveyResponse.objects.filter(department_id__name__iexact=department_name)

        if queryset.count() < 5:
            return Response({"detail": "Not enough data for analytics"}, status=status.HTTP_403_FORBIDDEN)

        return Response(get_department_analytics(department_name, queryset), status=status.HTTP_200_OK)
    
class OverallAnalyticsAPIView(APIView):
    '''API view for overall analytics data'''

    permission_classes = [IsHR]

    @extend_schema(
        description="Retrieves aggregated survey scores across all departments. Requires a minimum of 5 responses for privacy.",
        responses={
            200: OverallAnalyticsResponseSerializer,
            403: OpenApiResponse(description="Not enough data for analytics (less than 5 responses).")
        }
    )

    def get(self, request):
        '''Handle GET request for overall analytics data'''
        return Response(get_analytics(), status=status.HTTP_200_OK)

