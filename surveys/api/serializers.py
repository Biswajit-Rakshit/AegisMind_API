from rest_framework import serializers
from surveys.models import SurveyResponse

from accounts.models import Department, User

class SurveyResponseSerializer(serializers.ModelSerializer):
    '''Serializer for the SurveyResponse model'''

    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), allow_null=True)
    class Meta:
        model = SurveyResponse
        fields = ['id', 'user_id', 'department_id', 'stress_score', 'workload_score', 'mood_score', 'burnout_score', 'submitted_at']
        read_only_fields = ['id','user_id', 'department_id','submitted_at']