from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(employee_store)


class VerificationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'overAll_status')
admin.site.register(verification_store,VerificationAdmin)