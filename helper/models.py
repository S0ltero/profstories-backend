from django.db import models


class Mission(models.Model):
    coins = models.PositiveIntegerField(verbose_name="Монеты")
    order = models.PositiveIntegerField(verbose_name="Номер миссии", unique=True)

    class Meta:
        verbose_name = "Миссия"
        verbose_name_plural = "Миссии"
