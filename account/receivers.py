from django.dispatch import receiver
from django.contrib.auth import get_user_model

from djoser.signals import user_registered

from .email import TeacherRegisterEmail

User = get_user_model()

@receiver(user_registered)
def user_registered(sender, user, request, **kwargs):
    if user.type == User.Types.TEACHER:
        context = {"user": user}
        to = [user.email]
        TeacherRegisterEmail(request, context).send(to)
