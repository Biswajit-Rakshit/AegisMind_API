from surveys.models import SurveyResponse
from django.db import models
from django.db.models import Avg, Count

def get_analytics():
    response_list = SurveyResponse.objects.values(
            departments=models.F('department_id__name')).annotate(
            response_count=Count('id'),
            avg_stress=Avg('stress_score'),
            avg_workload=Avg('workload_score'),
            avg_mood=Avg('mood_score'),
            avg_burnout=Avg('burnout_score')
        ).filter(response_count__gte=5)
    response_list['avg_stress'] = round(response_list['avg_stress'], 2)
    response_list['avg_workload'] = round(response_list['avg_workload'], 2)
    response_list['avg_mood'] = round(response_list['avg_mood'], 2)
    response_list['avg_burnout'] = round(response_list['avg_burnout'], 2)
    return response_list

def get_department_analytics(department_name, queryset):

    data = queryset.aggregate(
            response_count=Count('id'),
            avg_stress_score=Avg('stress_score'),
            avg_workload_score=Avg('workload_score'),
            avg_mood_score=Avg('mood_score'),
            avg_burnout_score=Avg('burnout_score'),
        )
    data['department'] = department_name
    data['avg_stress_score'] = round(data['avg_stress_score'], 2)
    data['avg_workload_score'] = round(data['avg_workload_score'], 2)
    data['avg_mood_score'] = round(data['avg_mood_score'], 2)
    data['avg_burnout_score'] = round(data['avg_burnout_score'], 2)
    return data