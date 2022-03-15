from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from templated_mail.mail import BaseEmailMessage

from djoser import email

class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "email/password_reset.html"

    def get_context_data(self):
        # PasswordResetEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = email.utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.DJOSER["PASSWORD_RESET_CONFIRM_URL"].format(**context)
        return context


class TeacherRegisterEmail(BaseEmailMessage):
    template_name = "email/teacher_register.html"

    def get_context_data(self):
        context = super().get_context_data()
        return context