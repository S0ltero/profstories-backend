from django.contrib import admin

from .models import *
@admin.register(Employer)
class AdminEmployer(admin.ModelAdmin):
    actions = None
    list_display = ("user", "company_name")
    fieldsets = (
        ("Представитель",
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
