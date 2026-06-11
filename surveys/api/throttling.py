from datetime import timedelta
from django.utils import timezone
from rest_framework.throttling import BaseThrottle

from surveys.models import SurveyResponse

class OncePerCalendarWeekThrottle(BaseThrottle):
    def allow_request(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return True

        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        already_submitted = SurveyResponse.objects.filter(
            user_id=request.user,
            submitted_at__date__gte=start_of_week,
            submitted_at__date__lte=end_of_week
        ).exists()

        return not already_submitted