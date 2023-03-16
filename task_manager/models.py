from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from it_company import settings


class TaskType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="workers")

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return f"{get_user_model().username}"


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("LOW", "Low"),
        ("AVERAGE", "Average"),
        ("HIGH", "High"),
        ("URGENT", "Urgent"),
    )

    name = models.CharField(max_length=63)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField()
    priority = models.CharField(max_length=12, choices=PRIORITY_CHOICES, default="LOW")

    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasks")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
