from django.db import models
from django.db.models import Avg, Count

from surveys.models import SurveyResponse
from accounts.models import Department

def get_department_analytics(department_name, queryset, start_date, end_date):
    '''Calculate and return analytics data for a specific department'''

    if not Department.objects.filter(name__iexact=department_name).exists():
        raise Department.DoesNotExist

    department_queryset = queryset.filter(department_id__name__iexact=department_name)

    metrics = department_queryset.aggregate(
            response_count=Count('id'),
            avg_stress_score=Avg('stress_score'),
            avg_workload_score=Avg('workload_score'),
            avg_mood_score=Avg('mood_score'),
            avg_burnout_score=Avg('burnout_score'),
        )
    
    if metrics['response_count'] < 5:
        raise ValueError("Not enough data for analytics")
    
    return {
        'department': department_name,
        'start_date': start_date,
        'end_date': end_date,
        'response_count': metrics['response_count'],
        'avg_stress_score': round(metrics['avg_stress_score'], 2),
        'avg_workload_score': round(metrics['avg_workload_score'], 2),
        'avg_mood_score': round(metrics['avg_mood_score'], 2),
        'avg_burnout_score': round(metrics['avg_burnout_score'], 2),
    }

def get_analytics(queryset, start_date, end_date):
    '''Calculate and return analytics data for all departments'''

    response_list = queryset.values(
            department_name=models.F('department_id__name')).annotate(
            response_count=Count('id'),
            avg_stress=Avg('stress_score'),
            avg_workload=Avg('workload_score'),
            avg_mood=Avg('mood_score'),
            avg_burnout=Avg('burnout_score')
        ).filter(response_count__gte=5)
    
    cleaned_data = []
    for item in response_list:
        cleaned_data.append({
            'department': item['department_name'],
            'start_date': start_date,
            'end_date': end_date,
            'response_count': item['response_count'],
            'avg_stress_score': round(item['avg_stress'] or 0, 2),
            'avg_workload_score': round(item['avg_workload'] or 0, 2),
            'avg_mood_score': round(item['avg_mood'] or 0, 2),
            'avg_burnout_score': round(item['avg_burnout'] or 0, 2),
        })

    return cleaned_data

