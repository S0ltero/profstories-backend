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


class UserResource(resources.ModelResource):
    class Meta:
        model = UserExport

# Admin models

@admin.register(EmployerExport)
class AdminEmployer(ImportExportActionModelAdmin):
    resource_class = EmployerResource
    actions = None
    list_display = ("user", "fullname", "verification")

    @admin.display(description="Полное имя")
    def fullname(self, obj):
        return str(f"{obj.user.last_name} {obj.user.first_name} {obj.user.middle_name}")

    @admin.display(description="Уровень верификации")
    def verification(self, obj):
        return str(obj.user.get_verification_display())


@admin.register(ProfessionalExport)
class AdminProfessional(ImportExportActionModelAdmin):
    resource_class = ProfessionalResource
    actions = None
    list_display = ("user", "fullname", "verification")

    @admin.display(description="Полное имя")
    def fullname(self, obj):
        return str(f"{obj.user.last_name} {obj.user.first_name} {obj.user.middle_name}")

    @admin.display(description="Уровень верификации")
    def verification(self, obj):
        return str(obj.user.get_verification_display())
