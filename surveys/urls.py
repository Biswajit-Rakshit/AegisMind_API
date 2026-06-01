from django.urls import include, path

from surveys.api.views import SurveyResponseCreateView

urlpatterns = [
    path('survey-submit/', SurveyResponseCreateView.as_view(), name='survey-submit'),
]