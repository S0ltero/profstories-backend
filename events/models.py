from django.db import models
from django.contrib.postgres.fields import ArrayField

from account.models import Employer
class Event(models.Model):
    class Modes(models.Choices):
        ONLINE = "ONLINE", "Online"
        OFFLINE = "OFFLINE", "Offline"
        MIXED = "MIXED", "Mixed"

    class Periodic(models.Choices):
        FIRST = "FIRST", "Впервые"
        MONTH = "MONTH", "Ежемесячный"
        QUART = "QUART", "Ежеквартальный"
        YEAR = "YEAR", "Ежегодный"

    class Verifiaction(models.Choices):
        CREATED = "CREATED", "Создано"
        MODERATION = "MODERATION", "На модерации"
        VERIFIED = "VERIFIED", "Верифицировано"

    employer = models.ForeignKey(Employer, verbose_name="Организация", on_delete=models.CASCADE, related_name="events")
    title = models.CharField(verbose_name="Название мероприятия", max_length=255)
    photo = models.ImageField(verbose_name="Фото мероприятия")
    description = models.TextField(verbose_name="Краткое описание мероприятия")
    format = models.CharField(verbose_name="Формат мероприятия", max_length=255)
    date = models.DateTimeField(verbose_name="Дата проведения")
    profile = models.CharField(verbose_name="Профиль мероприятия", max_length=255)
    mode = models.CharField(verbose_name="Режим мероприятия", max_length=255, choices=Modes.choices)
    address = models.TextField(verbose_name="Адрес проведения")
    geography = ArrayField(models.CharField(max_length=255), verbose_name="География проведения")
    territorial_limits = models.TextField(verbose_name="Территориальные ограничения")
    url = models.URLField(verbose_name="Ссылка на сайт")
    audience = models.CharField(verbose_name="Целевая аудитория", max_length=255)
    audience_level = models.CharField(verbose_name="Класс/возраст школьников", max_length=255)
    periodic = models.CharField(verbose_name="Периодичность проведения", max_length=255, choices=Periodic.choices)
    regularity = models.CharField(verbose_name="Регулярность проведения", max_length=255)
    is_free = models.BooleanField(verbose_name="Бесплатно?")
    has_retreat = models.BooleanField(verbose_name="Возможность проведения выездного мероприятия?")
    certificates = models.TextField(verbose_name="Сертификаты")
    speakers = models.TextField(verbose_name="Спикеры")
    additional_info = models.TextField(verbose_name="Дополнительная информация")
    video = models.URLField(verbose_name="Видео о мероприятии")
    verification = models.CharField(
        verbose_name="Уровень верификации",
        max_length=50,
        choices=Verifiaction.choices,
        default=Verifiaction.CREATED
    )

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"