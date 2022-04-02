from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

from .models import (
    EmployerExport,
    ProfessionalExport,
    EmploymentAgencyExport,
    CollegeExport,
    NPOExport,
    TeacherExport,
    UserExport,
    EventExport
)

# Resources

class EmployerResource(resources.ModelResource):
    class Meta:
        model = EmployerExport
        import_id_fields = ("user",)


class ProfessionalResource(resources.ModelResource):
    class Meta:
        model = ProfessionalExport
        import_id_fields = ("user",)


class EmploymentAgencyResource(resources.ModelResource):
    class Meta:
        model = EmploymentAgencyExport
        import_id_fields = ("user",)


class CollegeResource(resources.ModelResource):
    class Meta:
        model = CollegeExport
        import_id_fields = ("user",)


class NPOResource(resources.ModelResource):
    class Meta:
        model = NPOExport
        import_id_fields = ("user",)


class TeacherResource(resources.ModelResource):
    class Meta:
        model = TeacherExport
        import_id_fields = ("user",)


class UserResource(resources.ModelResource):
    class Meta:
        model = UserExport


class EventResource(resources.ModelResource):
    class Meta:
        model = EventExport


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


@admin.register(TeacherExport)
class AdminTeacher(ImportExportActionModelAdmin):
    resource_class = TeacherResource
    actions = None
    list_display = ("user", "fullname", "verification")

    @admin.display(description="Полное имя")
    def fullname(self, obj):
        return str(f"{obj.user.last_name} {obj.user.first_name} {obj.user.middle_name}")

    @admin.display(description="Уровень верификации")
    def verification(self, obj):
        return str(obj.user.get_verification_display())


@admin.register(UserExport)
class AdminUser(ImportExportActionModelAdmin):
    resource_class = UserResource
    actions = None
    list_display = ("id", "email", "last_name", "first_name", "middle_name", "verification")
    list_display_links = ("id", "email")
    list_filter = ("type", "verification")
    exclude = ("password", "is_active", "is_staff", "is_superuser",
               "last_login", "date_joined", "user_permissions", "groups")


@admin.register(EventExport)
class AdminEvent(ImportExportActionModelAdmin):
    resource_class = EventResource
    actions = None