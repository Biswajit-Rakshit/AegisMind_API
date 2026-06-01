from rest_framework import serializers
from surveys.models import SurveyResponse

class SurveyResponseSerializer(serializers.ModelSerializer):
    '''Serializer for the SurveyResponse model'''
    class Meta:
        model = SurveyResponse
        fields = '__all__'
        read_only_fields = ['id','user_id', 'department_id','submitted_at']