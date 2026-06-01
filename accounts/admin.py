from django.contrib import admin

from accounts.models import User, Department

# Register your models here.
admin.site.register(User)
admin.site.register(Department)
