from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class SurveyResponse(models.Model):
    '''Model representing a survey response submitted by an employee'''
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    department_id = models.ForeignKey('accounts.Department', on_delete=models.SET_NULL, null=True)
    stress_score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    workload_score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    mood_score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    burnout_score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Survey response by {self.user_id.email} on {self.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}"