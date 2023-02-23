from django.contrib import admin
from .models import *


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'created_date', 'updated_date')
admin.site.register(employee_store,EmployeeAdmin)

class VerificationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'overAll_status')
admin.site.register(admin_store,VerificationAdmin)


class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('candidate_obj', 'admin_store', 'document_type', 'uploader_type')
admin.site.register(documents_store,DocumentsAdmin)