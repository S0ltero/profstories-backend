from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


class Event(models.Model):
    class Modes(models.TextChoices):
        ONLINE = "ONLINE", "Онлайн"
        OFFLINE = "OFFLINE", "Оффлайн"
        MIXED = "MIXED", "Смешанный"

    class Periodic(models.TextChoices):
        FIRST = "FIRST", "Впервые"
        MONTH = "MONTH", "Ежемесячный"
        QUART = "QUART", "Ежеквартальный"
        YEAR = "YEAR", "Ежегодный"

    class Verifiaction(models.TextChoices):
        MODERATION = "MODERATION", "На модерации"
        VERIFIED = "VERIFIED", "Верифицировано"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Организатор", on_delete=models.CASCADE, related_name="events")
    title = models.CharField(verbose_name="Название мероприятия", max_length=255)
    title_other = models.CharField(verbose_name="Другое название мероприятия", max_length=255, blank=True)
    photo = models.ImageField(verbose_name="Фото мероприятия", upload_to="events")
    description = models.TextField(verbose_name="Краткое описание мероприятия")
    description_other = models.TextField(verbose_name="Другое краткое описание мероприятия", blank=True)
    format = models.CharField(verbose_name="Формат мероприятия", max_length=255)
    format_other = models.CharField(verbose_name="Другой формат мероприятия", max_length=255, blank=True)
    date = models.DateTimeField(verbose_name="Дата проведения")
    profile = models.CharField(verbose_name="Профиль мероприятия", max_length=255)
    mode = models.CharField(verbose_name="Режим мероприятия", max_length=255, choices=Modes.choices)
    address = models.TextField(verbose_name="Адрес проведения")
    address_other = models.TextField(verbose_name="Другой адрес проведения", blank=True)
    geography = ArrayField(models.CharField(max_length=255), verbose_name="География проведения")
    territorial_limits = models.TextField(verbose_name="Территориальные ограничения")
    url = models.URLField(verbose_name="Ссылка на сайт")
    audience = models.CharField(verbose_name="Целевая аудитория", max_length=255)
    audience_level = models.CharField(verbose_name="Класс/возраст школьников", max_length=255)
    audience_level_other = models.CharField(verbose_name="Другой класс/возраст школьников", max_length=255, blank=True)
    periodic = models.CharField(verbose_name="Периодичность проведения", max_length=255, choices=Periodic.choices)
    regularity = models.CharField(verbose_name="Регулярность проведения", max_length=255)
    is_free = models.BooleanField(verbose_name="Бесплатно?")
    has_retreat = models.BooleanField(verbose_name="Возможность проведения выездного мероприятия?")
    certificates = models.TextField(verbose_name="Сертификаты")
    speakers = models.TextField(verbose_name="Спикеры")
    additional_info = models.TextField(verbose_name="Дополнительная информация")
    video = models.URLField(verbose_name="Видео о мероприятии", blank=True)
    verification = models.CharField(
        verbose_name="Уровень верификации",
        max_length=50,
        choices=Verifiaction.choices,
        default=Verifiaction.MODERATION
    )

    whitelist = models.BooleanField(verbose_name="Белый список", default=False)

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
