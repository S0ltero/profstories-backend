from django.contrib import admin

from .models import *


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


class TeacherInline(admin.StackedInline):
    model = Teacher
    extra = 0


@admin.register(UserProfessional)
class AdminProfessional(admin.ModelAdmin):
    inlines = (ProfessionalInline, UploadInline)
    exclude = ("password", "is_active", "is_staff", "is_superuser",
               "last_login", "date_joined", "user_permissions", "groups")


@admin.register(UserEmployer)
class AdminEmployer(admin.ModelAdmin):
    inlines = [EmployerInline]
    exclude = ("password", "is_active", "is_staff", "is_superuser",
               "last_login", "date_joined", "user_permissions", "groups")


@admin.register(UserNPO)
class AdminNPO(admin.ModelAdmin):
    inlines = [NPOInline]
    exclude = ("password", "is_active", "is_staff", "is_superuser",
               "last_login", "date_joined", "user_permissions", "groups")


@admin.register(UserCollege)
class AdminCollege(admin.ModelAdmin):
    inlines = [CollegeInline]
    exclude = ("password", "is_active", "is_staff", "is_superuser",
               "last_login", "date_joined", "user_permissions", "groups")


@admin.register(UserEmploymentAgency)
class AdminEmploymentAgency(admin.ModelAdmin):
    inlines = [EmploymentAgencyInline]
    exclude = ("password", "is_active", "is_staff", "is_superuser",
               "last_login", "date_joined", "user_permissions", "groups")



@admin.register(UserTeacher)
class AdminTeacher(admin.ModelAdmin):
    inlines = [TeacherInline]
    exclude = ("password", "is_active", "is_staff", "is_superuser",
               "last_login", "date_joined", "user_permissions", "groups")
