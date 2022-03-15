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


class ProfessionalResource(resources.ModelResource):
    class Meta:
        model = ProfessionalExport


class TeacherResource(resources.ModelResource):
    class Meta:
        model = TeacherExport
