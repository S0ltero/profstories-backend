from collections import Counter

from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

from events.models import Event


class Mission(models.Model):
    coins = models.PositiveIntegerField(verbose_name="Монеты")
    order = models.PositiveIntegerField(verbose_name="Номер миссии", unique=True)

    class Meta:
        verbose_name = "Миссия"
        verbose_name_plural = "Миссии"

    def __str__(self) -> str:
        return f"Миссия #{self.order}"


class MissionQuestion(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField(verbose_name="Вопрос")
    order = models.PositiveIntegerField(verbose_name="Номер вопроса")
    answers = models.JSONField(verbose_name="Ответы", default=dict, blank=True)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        unique_together = ("mission", "order")

    def __str__(self) -> str:
        return self.question


class QuestionVideo(models.Model):
    question = models.ForeignKey(MissionQuestion, on_delete=models.CASCADE, related_name="videos")
    url = models.URLField(verbose_name="Ссылка на видео")
    text = models.TextField(verbose_name="Текст к видео")

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"


class StudentMission(models.Model):
    class Reaction(models.TextChoices):
        FIRE = "FIRE", "🔥"
        HEART = "HEART", "❤️"
        FIVE = "FIVE", "🖐"
        SAD = "SAD", "🙁"

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    student = models.ForeignKey("account.Student", on_delete=models.CASCADE, related_name="missions")
    stage = models.PositiveIntegerField(verbose_name="Стадия", default=0)
    answers = models.JSONField(verbose_name="Ответы", default=dict, blank=True)
    reaction = models.CharField(verbose_name="Реакция", max_length=255, choices=Reaction.choices, blank=True)
    is_complete = models.BooleanField(verbose_name="Пройдена?", default=False)
    is_unlocked = models.BooleanField(verbose_name="Разблокировано?", default=False)

    class Meta:
        verbose_name = "Миссия"
        verbose_name_plural = "Миссии"

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.mission.order == 1:
                self.is_unlocked = True
            return super().save(*args, **kwargs)

        self.stage = len(self.answers)

        super().save(*args, **kwargs)

        if self.is_complete:
            self.student.coins += self.mission.coins
            self.student.save()

            try:
                next_mission = StudentMission.objects.get(
                    student=self.student,
                    mission__order=(self.mission.order + 1)
                )
            except StudentMission.DoesNotExist:
                pass
            else:
                next_mission.is_unlocked = True
                next_mission.save()

        if not self.student.missions.exclude(is_complete=True).exists():
            self.student.completed_at = timezone.now()
            self.student.save()

        if not self.answers.items():
            return

        answer_data = []

        points_dict = {
            1: 52,
            2: 30,
            3: 7,
            4: 6,
            5: 5
        }
        roles = {
            "leader": "Лидер",
            "specialist": "Специалист",
            "idea": "Генератор идей",
            "party": "Душа компании",
            "expert": "Эксперт"
        }
        motivation = {
            "achievement": "Достиженческий",
            "process": "Процессный",
            "material": "Материальный",
            "ideological": "Идейный",
            "team": "Командный"
        }

        for question, answers in self.answers.items():
            question = self.mission.questions.get(question=question)
            data = []
            for answer in answers:
                if not question.answers.get(answer):
                    continue
                else:
                    data.extend(question.answers.get(answer))

            if any(x in data for x in roles.keys()):
                data.extend([key for key in roles.keys() if key not in data])

                for i, key in enumerate(data, start=1):
                    self.student.role[roles[key]] = points_dict[i]

                self.student.save()
                continue
            elif any(x in data for x in motivation.keys()):
                data.extend([key for key in motivation.keys() if key not in data])

                for i, key in enumerate(data, start=1):
                    self.student.motivation[motivation[key]] = points_dict[i]

                self.student.save()
                continue

            answer_data.extend(data)

        answer_data = Counter(answer_data)
        skills_bulk = []
        for value, count in answer_data.items():
            if value.startswith("entrepreneurship"):
                if value.endswith("1"):
                    self.student.entrepreneurship = 16
                elif value.endswith("2"):
                    self.student.entrepreneurship = 57
                else:
                    self.student.entrepreneurship = 87
                self.student.save()
                continue

            skill = self.student.skills.get(object=value.upper())
            skill.points = count
            skills_bulk.append(skill)

        StudentSkill.objects.bulk_update(skills_bulk, ["points"])


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


class SkillScope(models.Model):
    object = models.CharField(
        verbose_name="Объект",
        max_length=255,
        choices=StudentSkill.Object.choices,
        unique=True
    )
    scope = ArrayField(models.CharField(max_length=255), verbose_name="Сферы деятельности")

    class Meta:
        verbose_name = "Суперспособность"
        verbose_name_plural = "Суперспособности"

    def __str__(self) -> str:
        return self.get_object_display()


class StudentEvent(models.Model):
    student = models.ForeignKey("account.Student", on_delete=models.CASCADE, related_name="events")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="+")
