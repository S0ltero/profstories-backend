from django.db import models
from django.core import validators
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser

from .managers import UserManager

class User(AbstractUser):
    class Types(models.TextChoices):
        PROFESSIONAL = "PROFESSIONAL", "Профессионал"
        EMPLOYER = "EMPLOYER", "Организация"

    class Verifiaction(models.TextChoices):
        CREATED = "CREATED", "Создан"
        MODERATION = "MODERATION", "На модерации"
        VERIFIED = "VERIFIED", "Верифицирован"


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
        choices=Verifiaction.choices,
        default=Verifiaction.CREATED
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ()

    objects = UserManager()


class EmployerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.EMPLOYER)


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    post = models.CharField(verbose_name="Должность", max_length=255)
    phone = models.CharField(verbose_name="Мобильный телефон", max_length=255)
    work_phone = models.CharField(verbose_name="Рабочий телефон", max_length=255)
    authorization = models.FileField(verbose_name="Доверенность")
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
    has_adaptation = models.BooleanField(verbose_name="Имеется ли программа адаптации?", default=False)
    adaptation_stages = models.TextField(verbose_name="Стадии адаптации")

    # Support Programm
    support_programms = models.CharField(verbose_name="Программа поддержки", max_length=255)
    support_conditions = models.TextField(verbose_name="Условия поддержки")

    educational_institution = ArrayField(models.TextField(), verbose_name="Какие обр. учереждения необходимо закончить?")
    educational_courses = ArrayField(models.TextField(), verbose_name="Какие обр. направление необходимо закончить?")
    has_student_events = models.BooleanField(verbose_name="Проводит ли организация мероприятия для школьников/студентов?", default=False)

    soft_skils = ArrayField(models.CharField(max_length=255), verbose_name="Надпрофессиональные компетенции")
    has_work_practice = models.BooleanField(verbose_name="Есть ли практика?", default=False)
    has_educational_products = models.BooleanField(verbose_name="Есть ли образовательные продукты?", default=False)
    has_targeted_training = models.BooleanField(verbose_name="Есть ли целевое обучение?", default=False)

    objects = EmployerManager

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"


class ProfessionalManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.PROFESSIONAL)


class Professional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    region = models.CharField(verbose_name="Регион", max_length=255)
    locality = models.CharField(verbose_name="Населенный пункт", max_length=255)
    photo = models.ImageField(verbose_name="Фото")
    phone = models.CharField(verbose_name="Мобильный телефон", max_length=255)
    work_phone = models.CharField(verbose_name="Рабочий телефон", max_length=255)
    birth_date = models.DateField(verbose_name="Дата рождения")
    wage = models.CharField(verbose_name="Уровень заработной платы", max_length=255)
    jobs_count = models.IntegerField(verbose_name="Количество мест работы") # TODO Char field?
    speciality = models.CharField(verbose_name="Специальность по диплому", max_length=255)
    education = models.CharField(verbose_name="Образование", max_length=255)
    work_on_speciality = models.BooleanField(verbose_name="Работа по специальности")
    work_on_speciality_tips = models.TextField(verbose_name="Почему стоит работаь по специальности")
    graduation_exams = ArrayField(models.CharField(max_length=255), verbose_name="Экзаменационные предметы")
    films = models.TextField(verbose_name="Фильмы")
    books = models.TextField(verbose_name="Книги")
    profession_hobbies = ArrayField(models.CharField(max_length=100), verbose_name="Увлечения для профессии")
    profession_qualities = ArrayField(models.CharField(max_length=100), verbose_name="Качества необходимые для профессии")
    profession_technology = models.TextField(verbose_name="Техника использующаяся в профессии")
    educational_institution = models.CharField(verbose_name="Образовательное учереждение", max_length=255)
    required_professions_opinion = models.TextField(verbose_name="Мнение о востребованных профессиях")
    professional_competencies = models.TextField(verbose_name="Какие профессиональные компетенции потребуется в будущем?")
    not_required_professions_opinion = models.TextField(verbose_name="Какие профессии не будут востребованы в будущем?")
    soft_skils = models.TextField(verbose_name="Надпрофессиональные компетенции")
    is_ready_to_mentor = models.BooleanField(verbose_name="Готовность быть наставником")
    is_ready_to_excursion = models.BooleanField(verbose_name="Готовность к проведению экскурсии")
    is_ready_to_tell_about = models.BooleanField(verbose_name="Готовность рассказть о профессии")
    favorite_school_subjects = models.TextField(verbose_name="Любимые школьные предметы")

    # Work
    scope = models.TextField(verbose_name="Сфера деятельности") # TODO Array field?
    seniority = models.CharField(verbose_name="Стаж работы", max_length=100)
    timetable = models.CharField(verbose_name="График работы", max_length=255)
    profession_name = models.CharField(verbose_name="Название профессии", max_length=255)
    profession_definition = models.TextField(verbose_name="Определение профессии")
    employment_type = models.CharField(verbose_name="Тип занятости", max_length=100)
    business_trips = models.TextField(verbose_name="Командировки")
    time_of_work = models.CharField(verbose_name="Количество лет работы в организации", max_length=255)
    workplace_environment = models.TextField(verbose_name="Предметы окружения на работе")
    workplace_photo = models.ImageField(verbose_name="Фото рабочего места")
    workplace_video = models.URLField(verbose_name="Видео рабочего места")
    workday_description = models.TextField(verbose_name="Описание рабочего дня")
    workday_start = models.CharField(verbose_name="Начало рабочего дня", max_length=100) # TODO Time field?
    workday_end = models.CharField(verbose_name="Конец рабочего дня", max_length=100) # TODO Time field?
    work_difficulties = models.TextField(verbose_name="Трудности на работе")
    work_myths = models.TextField(verbose_name="Мифы и стереотипы о работе")
    how_find_work = models.TextField(verbose_name="Как нашел эту работу?")

    # Company
    company_name = models.ForeignKey(Employer, to_field="company_name", related_name="employees", on_delete=models.PROTECT)
    company_TIN = models.ForeignKey(Employer, to_field="company_TIN", related_name="employees_TIN", on_delete=models.PROTECT)
    # PWD - People With Disabilities
    has_pwd = models.BooleanField(verbose_name="Работают ли люди с ограниченными возможностями?")
    has_corporate_training = models.BooleanField(verbose_name="Имеется корпоративное обучение?")

    objects = ProfessionalManager

    class Meta:
        verbose_name = "Профессионал"
        verbose_name_plural = "Профессионалы"