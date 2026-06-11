from datetime import timedelta
from django.utils import timezone
from django_filters import FilterSet, DateFilter
from surveys.models import SurveyResponse

class SurveyAnalyticsFilter(FilterSet):
    '''Filtering out Start and End date of responses. By default it should show current week'''

    start_date = DateFilter(field_name="submitted_at", lookup_expr="date__gte")
    end_date = DateFilter(field_name="submitted_at",lookup_expr="date__lte")

    class Meta:
        model = SurveyResponse
        fields = ['start_date', 'end_date']

    @property
    def qs(self):
        parent = super().qs

        start_date = self.form.cleaned_data.get('start_date')
        end_date = self.form.cleaned_data.get('end_date')

        if not start_date and not end_date:
            today = timezone.now().date()

            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            return parent.filter(
                submitted_at__date__gte=start_of_week,
                submitted_at__date__lte=end_of_week
            )
        return parent
    
    def get_applied_dates(self):
        """
        Helper method to extract what date range was ultimately used 
        (either the user's custom dates or our generated fallback).
        """

        if not hasattr(self, '_qs'):
            _ = self.qs
            
        start_date = self.form.cleaned_data.get('start_date')
        end_date = self.form.cleaned_data.get('end_date')

        if not start_date and not end_date:
            today = timezone.now().date()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            return start_of_week, end_of_week

        return start_date, end_date
