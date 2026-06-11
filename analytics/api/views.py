from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter, OpenApiTypes

from analytics.api.service import get_analytics, get_department_analytics
from accounts.models import Department
from accounts.api.permissions import IsHR
from analytics.api.serializers import DepartmentAnalyticsResponseSerializer, OverallAnalyticsResponseSerializer
from analytics.api.filters import SurveyAnalyticsFilter
from surveys.models import SurveyResponse

class DepartmentAnalyticsAPIView(APIView):
    '''API view for analytics data'''

    permission_classes = [IsHR]

    @extend_schema(
        description="Retrieves aggregated survey scores for a specific department. Requires a minimum of 5 responses for privacy.",
        parameters=[
            OpenApiParameter(
                name='start_date', 
                type=OpenApiTypes.DATE, 
                location=OpenApiParameter.QUERY, 
                description="Filter responses from this date (YYYY-MM-DD). Defaults to the start of the current week if both dates are missing."
            ),
            OpenApiParameter(
                name='end_date', 
                type=OpenApiTypes.DATE, 
                location=OpenApiParameter.QUERY, 
                description="Filter responses up to this date (YYYY-MM-DD). Defaults to the end of the current week if both dates are missing."
            ),
        ],
        responses={
            200: DepartmentAnalyticsResponseSerializer,
            403: OpenApiResponse(description="Not enough data for analytics (less than 5 responses)."),
            404: OpenApiResponse(description="Department not found.")
        }
    )

    def get(self, request, department_name):
        '''Handle GET request for analytics data'''

        filter_set = SurveyAnalyticsFilter(request.GET, queryset=SurveyResponse.objects.all(), request=request)
        
        filtered_qs = filter_set.qs

        start_date, end_date = filter_set.get_applied_dates()

        try:
            analytics_data = get_department_analytics(department_name, filtered_qs, start_date, end_date)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Department.DoesNotExist:
            return Response({"detail": "Department not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(analytics_data, status=status.HTTP_200_OK)
    
class OverallAnalyticsAPIView(APIView):
    '''API view for overall analytics data'''

    permission_classes = [IsHR]

    @extend_schema(
        description="Retrieves aggregated survey scores across all departments. Requires a minimum of 5 responses for privacy.",
        parameters=[
            OpenApiParameter(
                name='start_date', 
                type=OpenApiTypes.DATE, 
                location=OpenApiParameter.QUERY, 
                description="Filter responses from this date (YYYY-MM-DD). Defaults to the start of the current week if both dates are missing."
            ),
            OpenApiParameter(
                name='end_date', 
                type=OpenApiTypes.DATE, 
                location=OpenApiParameter.QUERY, 
                description="Filter responses up to this date (YYYY-MM-DD). Defaults to the end of the current week if both dates are missing."
            ),
        ],
        responses={
            200: OverallAnalyticsResponseSerializer,
            403: OpenApiResponse(description="Not enough data for analytics (less than 5 responses).")
        }
    )

    def get(self, request):
        '''Handle GET request for overall analytics data'''

        filter_set = SurveyAnalyticsFilter(request.GET, queryset=SurveyResponse.objects.all(), request=request)
        
        filtered_qs = filter_set.qs

        start_date, end_date = filter_set.get_applied_dates()

        data = get_analytics(filtered_qs, start_date, end_date)
        if not data:
            return Response(
                {"detail": "Not enough data for analytics across any department."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return Response(data, status=status.HTTP_200_OK)

