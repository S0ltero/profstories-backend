from account.models import (
    Employer,
    Professional,
    Teacher,
    User
)


class UserExport(User):
    class Meta:
        proxy = True
        app_label = "export"
        verbose_name = User._meta.verbose_name
        verbose_name_plural = User._meta.verbose_name_plural

