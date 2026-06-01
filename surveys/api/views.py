from django.shortcuts import render
from rest_framework import generics

from surveys.models import SurveyResponse
from surveys.api.serializers import SurveyResponseSerializer
from accounts.api.permissions import IsEmployee

class SurveyResponseCreateView(generics.CreateAPIView):
    '''APIView for creating survey responses'''

    permission_classes = [IsEmployee]

    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer