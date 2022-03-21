from django.db import models


class Mission(models.Model):
    coins = models.PositiveIntegerField(verbose_name="Монеты")
    order = models.PositiveIntegerField(verbose_name="Номер миссии", unique=True)

    class Meta:
        verbose_name = "Миссия"
        verbose_name_plural = "Миссии"


class MissionQuestion(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField(verbose_name="Вопрос")
    order = models.PositiveIntegerField(verbose_name="Номер вопроса")
    answers = models.JSONField(verbose_name="Ответы")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        unique_together = ("mission", "order")

    def __str__(self) -> str:
        return self.question


class StudentSkill(models.Model):
    class Object(models.TextChoices):
        SOCIAL = "SOCIAL", "Работа с людьми"
        RESEARCH = "RESEARCH", "Иследовательская деятельность"
        PRACTIC = "PRACTIC", "Практическая деятельность"
        CREATIVE = "CREATIVE", "Творческая деятельность"
        EXTREMAL = "EXTREMAL", "Экстремальная деятельность"
        INFORMATION = "INFORMATION", "Работа с информацией"

    student = models.ForeignKey("account.Student", on_delete=models.CASCADE, related_name="skills")
    object = models.CharField(verbose_name="Объект", max_length=255, choices=Object.choices)
    points = models.PositiveIntegerField(verbose_name="Баллы", default=0)

    class Meta:
        verbose_name = "Суперспособность"
        verbose_name_plural = "Суперспособности"
