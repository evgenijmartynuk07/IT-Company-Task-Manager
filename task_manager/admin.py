from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import TaskType, Task, Worker, Position


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]

