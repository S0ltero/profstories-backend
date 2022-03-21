from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.type == User.Types.EMPLOYER


class IsProfessional(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.type == User.Types.PROFESSIONAL


class IsNPO(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.type == User.Types.NPO


class IsCollege(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.type == User.Types.COLLEGE


class IsEmploymentAgency(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.type == User.Types.EMPAGENCY


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.type == User.Types.STUDENT