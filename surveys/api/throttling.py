from rest_framework.throttling import UserRateThrottle

class SurveySubmissionThrottle(UserRateThrottle):
    '''Custom throttle class for survey submissions allowing raw seconds'''

    scope = 'survey_submission'

    def parse_rate(self, rate):
        """
        Overrides DRF's standard parsing to allow rates like '1/604800'
        where the denominator is just the total number of seconds.
        """
        if rate is None:
            return (None, None)
        
        num_requests, period = rate.split('/')
        num_requests = int(num_requests)
        
        if period.isdigit():
            return (num_requests, int(period))

        return super().parse_rate(rate)