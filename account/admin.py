from django.contrib import admin

import nested_admin

from helper.admin import StudentMissionInline, StudentSkillInline
from .models import *


admin.site.register(Callback)


class UploadInline(admin.StackedInline):
    model = Upload
    extra = 0


class ProfessionalInline(admin.StackedInline):
    model = Professional
    extra = 0


class EmployerInline(admin.StackedInline):
    model = Employer
    extra = 0

    fieldsets = (
        (None,
            {"fields": (
                "post", "phone", "work_phone", "authorization"
            )}
        ),
        ("Организация", {
                "fields": (
                    ("company_name", "company_name_alt"),
                    ("company_region", "company_admin_region"),
                    "company_description", "company_TIN", "company_scope",
                    "company_logo", "company_count_employees", "company_avg_wage",
                    "company_site", "company_video", "company_social", "company_professions",
                    "educational_institution", "educational_courses", "soft_skils",
                    "has_work_practice", "has_educational_products", "has_targeted_training"
                )
            }
        ),
        ("Корпоративное обучение",
            {"fields": (
                "has_corporate_training", "corporate_training_name"
            )}
        ),
        ("Программа адаптации",
            {"fields": (
                "has_adaptation", "adaptation_stages"
            )}
        ),
        ("Программа поддержки",
            {"fields": (
                "support_programms", "support_conditions"
            )}
        ),
        ("Люди с ограниченными возможностями",
            {"fields": (
                "has_pwd", "pwd_professions"
            )}
        ),
        ("Экскурсии", 
            {"fields": (
                "excursions", "excursion_employee_id",
                "excursion_employee_full_name", "excursion_employee_post"
            )}
        ),
        ("Взгляд в будущее",
            {"fields": (
                "professions_required", "professions_not_required",
                "professional_competencies"
            )}
        )
    )


class NPOInline(admin.StackedInline):
    model = NPO
    extra = 0


class CollegeInline(admin.StackedInline):
    model = College
    extra = 0


class EmploymentAgencyInline(admin.StackedInline):
    model = EmploymentAgency
    extra = 0


class TeacherStudentInline(nested_admin.NestedStackedInline):
    model = TeacherStudent
    extra = 0


class TeacherInline(nested_admin.NestedStackedInline):
    model = Teacher
    extra = 0
    inlines = (TeacherStudentInline,)


class StudentInline(nested_admin.NestedStackedInline):
    model = Student
    extra = 0
    inlines = (StudentMissionInline, StudentSkillInline)


@admin.register(UserProfessional)
class AdminProfessional(admin.ModelAdmin):
    inlines = (ProfessionalInline, UploadInline)
    actions = None
    list_display = ("id", "email", "last_name", "first_name", "middle_name", "verification")
    list_display_links = ("id", "email")
    list_filter = ("verification",)
    exclude = ("password", "is_active", "is_staff", "is_superuser",
               "last_login", "date_joined", "user_permissions", "groups")


@admin.register(UserEmployer)
class AdminEmployer(admin.ModelAdmin):
    inlines = (EmployerInline,)
    actions = None
    list_display = ("id", "email", "last_name", "first_name", "middle_name", "verification")
    list_display_links = ("id", "email")
    list_filter = ("verification",)
    exclude = ("password", "is_active", "is_staff", "is_superuser",
               "last_login", "date_joined", "user_permissions", "groups")


@admin.register(UserNPO)
class AdminNPO(admin.ModelAdmin):
    inlines = (NPOInline,)
    actions = None
    list_display = ("id", "email", "last_name", "first_name", "middle_name", "verification")
    list_display_links = ("id", "email")
    list_filter = ("verification",)
    exclude = ("password", "is_active", "is_staff", "is_superuser",
               "last_login", "date_joined", "user_permissions", "groups")


@admin.register(UserCollege)
class AdminCollege(admin.ModelAdmin):
    inlines = (CollegeInline,)
    actions = None
    list_display = ("id", "email", "last_name", "first_name", "middle_name", "verification")
    list_display_links = ("id", "email")
    list_filter = ("verification",)
    exclude = ("password", "is_active", "is_staff", "is_superuser",
               "last_login", "date_joined", "user_permissions", "groups")


@admin.register(UserEmploymentAgency)
class AdminEmploymentAgency(admin.ModelAdmin):
    inlines = (EmploymentAgencyInline,)
    actions = None
    list_display = ("id", "email", "last_name", "first_name", "middle_name", "verification")
    list_display_links = ("id", "email")
    list_filter = ("verification",)
    exclude = ("password", "is_active", "is_staff", "is_superuser",
               "last_login", "date_joined", "user_permissions", "groups")


@admin.register(UserTeacher)
class AdminTeacher(nested_admin.NestedModelAdmin):
    inlines = (TeacherInline,)
    actions = None
    list_display = ("id", "email", "last_name", "first_name", "middle_name", "verification")
    list_display_links = ("id", "email")
    list_filter = ("verification",)
    exclude = ("password", "is_active", "is_staff", "is_superuser",
               "last_login", "date_joined", "user_permissions", "groups")


@admin.register(UserStudent)
class AdminStudent(nested_admin.NestedModelAdmin):
    inlines = (StudentInline,)
    actions = None
    list_display = ("id", "email", "last_name", "first_name", "middle_name", "verification")
    list_display_links = ("id", "email")
    list_filter = ("verification",)
    exclude = ("password", "is_active", "is_staff", "is_superuser",
               "last_login", "date_joined", "user_permissions", "groups")
