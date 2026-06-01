from django.contrib import admin
from surveys.models import SurveyResponse

# admin.site.register(SurveyResponse)

@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    # This hides the department field from the admin form so it cannot be manually changed
    exclude = ('department_id',)

    def save_model(self, request, obj, form, change):
        # Automatically grab the department from the user before saving
        # This assumes your SurveyResponse model has a 'user' field 
        # and the User model has a 'department' field
        obj.department_id = obj.user_id.department
        super().save_model(request, obj, form, change)