from rest_framework import serializers

class DepartmentAnalyticsResponseSerializer(serializers.Serializer):
    '''Serializer for analytics data'''

    department = serializers.CharField(source='department_id__name')
    response_count = serializers.IntegerField()
    stress_score = serializers.FloatField()
    workload_score = serializers.FloatField()
    mood_score = serializers.FloatField()
    burnout_score = serializers.FloatField()

class OverallAnalyticsResponseSerializer(serializers.Serializer):
    '''Serializer for overall analytics data'''

    department = serializers.CharField(source='department__name')
    response_count = serializers.IntegerField()
    stress_score = serializers.FloatField()
    workload_score = serializers.FloatField()
    mood_score = serializers.FloatField()
    burnout_score = serializers.FloatField()