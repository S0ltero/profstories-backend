from account.models import (
    Employer,
    Professional,
    EmploymentAgency,
    College,
    NPO,
    Teacher,
    User
)
from events.models import Event


class UserExport(User):
    class Meta:
        proxy = True
        app_label = "export"
        verbose_name = User._meta.verbose_name
        verbose_name_plural = User._meta.verbose_name_plural


class EmployerExport(Employer):
    class Meta:
        proxy = True
        app_label = "export"
        verbose_name = Employer._meta.verbose_name
        verbose_name_plural = Employer._meta.verbose_name_plural


class ProfessionalExport(Professional):
    class Meta:
        proxy = True
        app_label = "export"
        verbose_name = Professional._meta.verbose_name
        verbose_name_plural = Professional._meta.verbose_name_plural


class EmploymentAgencyExport(EmploymentAgency):
    class Meta:
        proxy = True
        app_label = "export"
        verbose_name = EmploymentAgency._meta.verbose_name
        verbose_name_plural = EmploymentAgency._meta.verbose_name_plural


class CollegeExport(College):
    class Meta:
        proxy = True
        app_label = "export"
        verbose_name = College._meta.verbose_name
        verbose_name_plural = College._meta.verbose_name_plural


class NPOExport(NPO):
    class Meta:
        proxy = True
        app_label = "export"
        verbose_name = NPO._meta.verbose_name
        verbose_name_plural = NPO._meta.verbose_name_plural


class TeacherExport(Teacher):
    class Meta:
        proxy = True
        app_label = "export"
        verbose_name = Teacher._meta.verbose_name
        verbose_name_plural = Teacher._meta.verbose_name_plural


class EventExport(Event):
    class Meta:
        proxy = True
        app_label = "export"
        verbose_name = Event._meta.verbose_name
        verbose_name_plural = Event._meta.verbose_name_plural
