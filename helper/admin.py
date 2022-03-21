from django.db import models
from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget

import nested_admin

from .models import *


class StudentMissionInline(nested_admin.NestedStackedInline):
    model = StudentMission
    extra = 0
    classes = ["collapse"]

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
