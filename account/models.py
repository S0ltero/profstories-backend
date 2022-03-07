import string

from django.db import models
from django.core import validators
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.crypto import get_random_string

from .managers import UserManager


class User(AbstractUser):
    class Types(models.TextChoices):
        PROFESSIONAL = "PROFESSIONAL", "Профессионал"
        EMPLOYER = "EMPLOYER", "Организация"
        NPO = "NPO", "НКО"
        EMPAGENCY = "EMPAGENCY", "Орган занятости"
        COLLEGE = "COLLEGE", "ССУЗ"

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
        default=Verifiaction.CREATED,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ()

    objects = UserManager()


class EmployerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user__type=User.Types.EMPLOYER)


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
    company_region = ArrayField(models.CharField(max_length=255), verbose_name="Регион организации")
    company_admin_region = ArrayField(models.CharField(max_length=255), blank=True, default=list, verbose_name="Административный регион организации")
    company_scope = models.TextField(verbose_name="Сфера деятельности")
    company_logo = models.ImageField(verbose_name="Логотип организации")
    company_TIN = models.CharField(verbose_name="ИНН организации", max_length=10, unique=True)
    company_description = models.TextField(verbose_name="Об организации")
    company_count_employees = models.CharField(verbose_name="Число сотрудников", max_length=255)
    company_avg_wage = models.PositiveIntegerField(verbose_name="Средняя заработная плата")
    company_site = models.URLField(verbose_name="Сайт организации")
    company_video = models.URLField(verbose_name="Видео", blank=True, null=True)
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
    has_corporate_training = models.BooleanField(verbose_name="Имеется корпоративное обучение?", default=False)
    corporate_training_name = models.CharField(verbose_name="Название программы корпоративного обучения", max_length=255, blank=True)

    # Look into the future
    professions_required = ArrayField(models.CharField(max_length=255), verbose_name="В будущем востребованные профессии")
    professions_not_required = ArrayField(models.CharField(max_length=255), verbose_name="В будущем не востребованные профессии", blank=True)
    professional_competencies = ArrayField(models.CharField(max_length=255), verbose_name="В будущем востребованные профессиональные компетенции")

    # Adaptation
    has_adaptation = models.BooleanField(verbose_name="Имеется ли программа адаптации?", default=False)
    adaptation_stages = models.TextField(verbose_name="Стадии адаптации")

    # Support Programm
    support_programms = ArrayField(models.CharField(max_length=255), blank=True, default=list, verbose_name="Программа поддержки")
    support_conditions = models.TextField(verbose_name="Условия поддержки", blank=True)

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

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.user.verification = User.Verifiaction.MODERATION
            self.user.save()
        return super().save(*args, **kwargs)


class ProfessionalManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user__type=User.Types.PROFESSIONAL)


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
    work_on_speciality_tips = models.TextField(verbose_name="Почему стоит работать по специальности")
    graduation_exams = ArrayField(models.CharField(max_length=255), verbose_name="Экзаменационные предметы")
    films = models.TextField(verbose_name="Фильмы")
    books = models.TextField(verbose_name="Книги")
    profession_hobbies = ArrayField(models.CharField(max_length=100), verbose_name="Увлечения для профессии")
    profession_qualities = ArrayField(models.CharField(max_length=100), verbose_name="Качества необходимые для профессии")
    profession_technology = models.TextField(verbose_name="Техника использующаяся в профессии")
    educational_institution = models.CharField(verbose_name="Образовательное учреждение", max_length=255)
    required_professions_opinion = models.TextField(verbose_name="Мнение о востребованных профессиях", blank=True)
    professional_competencies = models.TextField(verbose_name="Какие профессиональные компетенции потребуется в будущем?")
    not_required_professions_opinion = models.TextField(verbose_name="Какие профессии не будут востребованы в будущем?")
    soft_skils = ArrayField(models.CharField(max_length=255), verbose_name="Надпрофессиональные компетенции")
    is_ready_to_mentor = models.BooleanField(verbose_name="Готовность быть наставником")
    is_ready_to_excursion = models.BooleanField(verbose_name="Готовность к проведению экскурсии")
    is_ready_to_tell_about = models.BooleanField(verbose_name="Готовность рассказать о профессии")
    favorite_school_subjects = ArrayField(models.CharField(max_length=255), verbose_name="Любимые школьные предметы")

    # Work
    scope = ArrayField(models.TextField(), verbose_name="Сфера деятельности")
    seniority = models.CharField(verbose_name="Стаж работы", max_length=100)
    timetable = models.CharField(verbose_name="График работы", max_length=255)
    profession_name = models.CharField(verbose_name="Название профессии", max_length=255)
    profession_definition = models.TextField(verbose_name="Определение профессии")
    employment_type = models.CharField(verbose_name="Тип занятости", max_length=100)
    business_trips = models.TextField(verbose_name="Командировки")
    time_of_work = models.CharField(verbose_name="Количество лет работы в организации", max_length=255)
    workplace_environment = models.TextField(verbose_name="Предметы окружения на работе")
    workplace_video = models.URLField(verbose_name="Видео рабочего места", blank=True)
    workday_description = models.TextField(verbose_name="Описание рабочего дня")
    workday_start = models.CharField(verbose_name="Начало рабочего дня", max_length=100) # TODO Time field?
    workday_end = models.CharField(verbose_name="Конец рабочего дня", max_length=100) # TODO Time field?
    work_difficulties = models.TextField(verbose_name="Трудности на работе")
    work_myths = models.TextField(verbose_name="Мифы и стереотипы о работе")
    how_find_work = models.TextField(verbose_name="Как нашел эту работу?")

    # Company
    company_name = models.CharField(verbose_name="Название организации", max_length=255)
    company_TIN = models.CharField(verbose_name="ИНН организации", max_length=10)
    # PWD - People With Disabilities
    has_pwd = models.BooleanField(verbose_name="Работают ли люди с ограниченными возможностями?")
    has_corporate_training = models.BooleanField(verbose_name="Имеется корпоративное обучение?")

    objects = ProfessionalManager

    class Meta:
        verbose_name = "Профессионал"
        verbose_name_plural = "Профессионалы"

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.user.verification = User.Verifiaction.MODERATION
            self.user.save()
        return super().save(*args, **kwargs)


class NPOManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user__type=User.Types.NPO)


class NPO(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    post = models.CharField(verbose_name="Должность", max_length=255)
    phone = models.CharField(verbose_name="Мобильный телефон", max_length=255)
    work_phone = models.CharField(verbose_name="Рабочий телефон", max_length=255)
    authorization = models.FileField(verbose_name="Доверенность")
    privacy_policy = models.BooleanField(verbose_name="Политика конфиденциальности", default=False)

    # Company attributes
    company_name = models.CharField(verbose_name="Название организации", max_length=255, unique=True)
    company_region = models.CharField(verbose_name="Регион организации", max_length=255)
    company_TIN = models.CharField(verbose_name="ИНН организации", max_length=10, unique=True)
    company_address = models.TextField(verbose_name="Адрес организации")
    company_logo = models.ImageField(verbose_name="Логотип организации")
    company_director = models.CharField(verbose_name="ФИО руководителя", max_length=255)
    company_count_employees = models.CharField(verbose_name="Число сотрудников", max_length=255)
    company_avg_wage = models.PositiveIntegerField(verbose_name="Средняя заработная плата")
    company_site = models.URLField(verbose_name="Сайт организации")
    company_video = models.URLField(verbose_name="Видео", blank=True, null=True)
    company_social = ArrayField(models.URLField(), verbose_name="Социальные сети")
    company_professions = ArrayField(models.CharField(max_length=255), verbose_name="Востребованные профессии")
    
    objects = NPOManager

    class Meta:
        verbose_name = "НКО"
        verbose_name_plural = "НКО"

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.user.verification = User.Verifiaction.MODERATION
            self.user.save()
        return super().save(*args, **kwargs)


class CollegeManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user__type=User.Types.COLLEGE)


class College(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    post = models.CharField(verbose_name="Должность", max_length=255)
    phone = models.CharField(verbose_name="Мобильный телефон", max_length=255)
    work_phone = models.CharField(verbose_name="Рабочий телефон", max_length=255)
    authorization = models.FileField(verbose_name="Доверенность")

    # College attributes
    college_TIN = models.CharField(verbose_name="ИНН колледжа", max_length=10)
    college_logo = models.ImageField(verbose_name="Логотип колледжа")
    college_name = models.CharField(verbose_name="Название колледжа", max_length=255)
    college_address = models.TextField(verbose_name="Адрес колледжа")
    college_name_abr = models.CharField(verbose_name="Сокращенное название колледжа", max_length=255)
    college_description = models.TextField(verbose_name="Описание колледжа")
    college_region = models.CharField(verbose_name="Регион колледжа", max_length=255)
    college_site = models.URLField(verbose_name="Сайт колледжа")
    college_video = models.URLField(verbose_name="Видео о колледже")
    college_social = ArrayField(models.URLField(), blank=True, default=list, verbose_name="Социальные сети")
    college_employers = ArrayField(models.CharField(max_length=255), blank=True, default=list, verbose_name="Работадатели")

    # Educational
    educational_level = models.CharField(verbose_name="Уровень получаемого образования", max_length=255)
    educational_professions = ArrayField(models.CharField(max_length=255), blank=True, default=list, verbose_name="Профессии преподаваемые в колледже")
    educational_cost = models.PositiveSmallIntegerField(verbose_name="Стоимость обучения в год")

    # State-funded places
    has_state_funded_place = models.BooleanField(verbose_name="Есть ли бюджетные места?")
    count_state_funded_place = models.PositiveSmallIntegerField(verbose_name="Количество бюджетных мест", blank=True)

    # Events
    has_events = models.BooleanField(verbose_name="Проводятся ли профориентационные мероприятия?")
    event_types = ArrayField(models.CharField(max_length=255), blank=True, default=list, verbose_name="Виды мероприятий")
    event_regularity = models.CharField(max_length=255, verbose_name="Частота мероприятий", blank=True)
    event_format = models.CharField(max_length=255, verbose_name="Формат мероприятий", blank=True)
    event_employer_name = models.CharField(max_length=255, verbose_name="ФИО сотрудника по мероприятиям", blank=True)
    event_employer_post = models.CharField(max_length=255, verbose_name="Должность сотрудника по мероприятиям", blank=True)
    event_employer_phone = models.CharField(max_length=255, verbose_name="Номер телефона сотрудника по мепроприятиям", blank=True)

    # Graduates monitoring
    has_monitoring = models.BooleanField(verbose_name="Проводится ли мониторинг трудоустройства выпускников?")
    monitoring_url = models.URLField(verbose_name="Ссылка на данные мониторинга", blank=True)
    employment_percent = models.CharField(max_length=255, verbose_name="Какой процент выпускников трудоустраивается в первый год?", blank=True)

    # Special conditions
    has_special_conditions = models.BooleanField(verbose_name="Имеются ли особые условия поступления")
    special_conditions = models.TextField(verbose_name="Особые условия поступления", blank=True)

    has_dormitory = models.BooleanField(verbose_name="Есть ли общежитие?")
    famous_graduates = ArrayField(models.CharField(max_length=255), verbose_name="Известные выпускники")
    has_foreign_practice = models.BooleanField(verbose_name="Наличие зарубежной практики")
    has_targeted_training = models.BooleanField(verbose_name="Возможно ли поступление по целевому обучению")
    has_pwd_education = models.BooleanField(verbose_name="Обучение студентов с ограниченными возможностями")
    extracurricular_activity = ArrayField(models.TextField(), verbose_name="Внеучебная работа")

    objects = CollegeManager()

    class Meta:
        verbose_name = "ССУЗ"
        verbose_name_plural = "ССУЗы"

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.user.verification = User.Verifiaction.MODERATION
            self.user.save()
        return super().save(*args, **kwargs)


class EmploymentAgencyManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user__type=User.Types.EMPAGENCY)


class EmploymentAgency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    post = models.CharField(verbose_name="Должность", max_length=255)
    phone = models.CharField(verbose_name="Мобильный телефон", max_length=255)
    work_phone = models.CharField(verbose_name="Рабочий телефон", max_length=255)
    authorization = models.FileField(verbose_name="Доверенность")

    company_TIN = models.CharField(verbose_name="ИНН организации", max_length=10, unique=True)
    company_name = models.CharField(verbose_name="Название организации", max_length=255)
    company_name_abr = models.CharField(verbose_name="Сокращенное название организации", max_length=255, blank=True)
    company_region = models.CharField(verbose_name="Регион организации", max_length=255)
    company_address = models.TextField(verbose_name="Адрес организации")
    company_site = models.URLField(verbose_name="Сайт организации")

    objects = EmploymentAgencyManager()

    class Meta:
        verbose_name = "Орган занятости"
        verbose_name_plural = "Органы занятости"

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.user.verification = User.Verifiaction.MODERATION
            self.user.save()
        return super().save(*args, **kwargs)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    post = models.CharField(verbose_name="Должность", max_length=255)
    region = models.CharField(verbose_name="Регион", max_length=255)
    locality = models.CharField(verbose_name="Населенный пункт", max_length=255)
    phone = models.CharField(verbose_name="Номер телефона", max_length=255)
    count_members = models.IntegerField(verbose_name="Количество участников")
    school_name = models.TextField(verbose_name="Название образовательной организации")
    code = models.CharField(verbose_name="Код", max_length=6)

    class Meta:
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.code = get_random_string(6, allowed_chars=string.ascii_uppercase + string.digits)
        super().save(*args, **kwargs)


class Upload(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", related_name="uploads", on_delete=models.CASCADE)
    file = models.FileField(verbose_name="Файл")
    type = models.CharField(verbose_name="Тип загрузки", max_length=70)

    class Meta:
        verbose_name = "Загрузка"
        verbose_name_plural = "Загрузки"


class Callback(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=255)
    email = models.EmailField(verbose_name="Почта")
    phone = models.CharField(verbose_name="Номер телефона", max_length=255)
    text = models.TextField(verbose_name="Текст")

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"


# Proxy models
class UserEmaployerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.EMPLOYER)


class UserEmployer(User):

    objects = UserEmaployerManager()

    class Meta:
        proxy = True
        verbose_name = "Организация"
        verbose_name_plural = "Организации"


class UserProfessionalManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.PROFESSIONAL)


class UserProfessional(User):

    objects = UserProfessionalManager()

    class Meta:
        proxy = True
        verbose_name = "Профессионал"
        verbose_name_plural = "Профессионалы"

class UserNPOManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.NPO)


class UserNPO(User):

    objects = UserNPOManager()

    class Meta:
        proxy = True
        verbose_name = "НКО"
        verbose_name_plural = "НКО"


class UserCollegeManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.COLLEGE)


class UserCollege(User):

    objects = UserCollegeManager()

    class Meta:
        proxy = True
        verbose_name = "ССУЗ"
        verbose_name_plural = "ССУЗы"


class UserEmploymentAgencyManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.EMPAGENCY)


class UserEmploymentAgency(User):

    objects = UserEmploymentAgencyManager()

    class Meta:
        proxy = True
        verbose_name = "Орган занятости"
        verbose_name_plural = "Органы занятости"
