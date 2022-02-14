from django.db import models
from django.core import validators
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser

from .managers import UserManager

class User(AbstractUser):
    class Types(models.TextChoices):
        PROFESSIONAL = "PROFESSIONAL", "Professional"
        EMPLOYER = "EMPLOYER", "Employer"


    CREATED = "CREATED"
    MODERATION = "MODERATION"
    VERIFIED = "VERIFIED"
    VERIFICATION_LEVEL_CHOICES = [
        (CREATED, "created"),
        (MODERATION, "on_moderation"),
        (VERIFIED, "verified")
    ]

    username = None
    email = models.EmailField(
        "Email адрес",
        unique=True,
        validators=[validators.validate_email],
        error_messages={
            "unique": "Пользователь с таким email уже существует.",
        },
    )
    type = models.CharField(verbose_name="Тип", max_length=50, choices=Types.choices)

    first_name = models.CharField(verbose_name="Имя", max_length=100)
    last_name = models.CharField(verbose_name="Фамилия", max_length=100)
    middle_name = models.CharField(verbose_name="Отчество", max_length=100, blank=True)
    verification = models.CharField(
        verbose_name="Уровень верификации",
        max_length=50,
        choices=VERIFICATION_LEVEL_CHOICES,
        default=CREATED
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ()

    objects = UserManager()


class EmployerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.EMPLOYER)


class Employer(models.Model):
    VERIFICATION_LEVEL_CHOICES = [
        ("CREATED", "created"),
        ("NOT_VERIFIED", "not_verified"),
        ("VERIFIED", "verified")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    post = models.CharField(verbose_name="Должность", max_length=255)
    phone = models.CharField(verbose_name="Мобильный телефон", max_length=255)
    work_phone = models.CharField(verbose_name="Рабочий телефон", max_length=255)
    authorization = models.FileField(verbose_name="Доверенность", max_length=255)
    privacy_policy = models.BooleanField(verbose_name="Политика конфиденциальности", default=False)

    # Company attributes
    company_name = models.CharField(verbose_name="Название организации", max_length=255, unique=True)
    company_name_alt = models.CharField(verbose_name="Альтернативное название организации", max_length=255, unique=True)
    company_region = models.CharField(verbose_name="Регион организации", max_length=255)
    company_admin_region = models.CharField(verbose_name="Административный регион организации", max_length=255)
    company_scope = models.TextField(verbose_name="Сфера деятельности")
    company_logo = models.ImageField(verbose_name="Логотип организации")
    company_TIN = models.CharField(verbose_name="ИНН организации", max_length=255, unique=True)
    company_description = models.TextField(verbose_name="Об организации")
    company_count_employees = models.CharField(verbose_name="Число сотрудников", max_length=255)
    company_avg_wage = models.IntegerField(verbose_name="Средняя заработная плата")
    company_site = models.URLField(verbose_name="Сайт организации")
    company_video = models.URLField(verbose_name="Видео")
    company_social = ArrayField(models.URLField(), verbose_name="Социальные сети")
    company_professions = ArrayField(models.CharField(max_length=255), verbose_name="Востребованные профессии")

    # PWD - People With Disabilities
    has_pwd = models.BooleanField(verbose_name="Работают ли люди с ограниченными возможностями?")
    pwd_professions = ArrayField(models.CharField(max_length=255), verbose_name="Профессии людей с ограниченными возможностями")

    # Excursions
    excursions = models.CharField(verbose_name="Экскурсии", max_length=255)
    excursion_employee_id = models.CharField(verbose_name="Номер сотрудника по экскурсии", max_length=255)
    excursion_employee_full_name = models.CharField(verbose_name="ФИО сотрудника по экскурсии", max_length=255)
    excursion_employee_post = models.CharField(verbose_name="Должность сотруднка по экскурсии", max_length=255)

    # Corporate Training
    has_corporate_training = models.BooleanField(verbose_name="Имеется корпоративное обучение?")
    corporate_training_name = models.CharField(verbose_name="Название программы корпоративного обучения", max_length=255)

    # Look into the future
    professions_required = ArrayField(models.CharField(max_length=255), verbose_name="В будущем востребованные профессии")
    professions_not_required = ArrayField(models.CharField(max_length=255), verbose_name="В будущем не востребованные профессии")
    professional_competencies = ArrayField(models.CharField(max_length=255), verbose_name="В будущем востребованные профессиональные компетенции")

    # Adaptation
    has_adaptation = models.BooleanField(default=False)
    adaptation_stages = models.TextField(verbose_name="Стадии адаптации")

    # Support Programm
    support_programms = models.CharField(verbose_name="Программа поддержки", max_length=255)
    support_conditions = models.TextField(verbose_name="Условия поддержки")

    educational_institution = ArrayField(models.TextField(), verbose_name="Какие обр. учереждения необходимо закончить?")
    educational_courses = ArrayField(models.TextField(), verbose_name="Какие обр. направление необходимо закончить?")

    soft_skils = ArrayField(models.CharField(max_length=255), verbose_name="Надпрофессиональные компетенции")
    has_work_practice = models.BooleanField(verbose_name="Есть ли практика?", default=False)
    has_educational_products = models.BooleanField(verbose_name="Есть ли образовательные продукты?", default=False)
    has_targeted_training = models.BooleanField(verbose_name="Есть ли целевое обучение?", default=False)


    objects = EmployerManager


class ProfessionalManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.PROFESSIONAL)

