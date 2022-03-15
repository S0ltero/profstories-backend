from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

from .models import (
    EmployerExport,
    ProfessionalExport,
    TeacherExport,
    UserExport
)

# Resources

class EmployerResource(resources.ModelResource):
    class Meta:
        model = EmployerExport
