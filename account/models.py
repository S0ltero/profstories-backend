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


