from django.urls import path

from analytics.views import DepartmentAnalyticsAPIView, OverallAnalyticsAPIView

urlpatterns = [
    path('all/', OverallAnalyticsAPIView.as_view(), name='overall-analytics'),
    path('<str:department_name>/', DepartmentAnalyticsAPIView.as_view(), name='department-analytics'),
]


