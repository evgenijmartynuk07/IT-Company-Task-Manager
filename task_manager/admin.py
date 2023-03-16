from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import TaskType, Task, Worker, Position


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
