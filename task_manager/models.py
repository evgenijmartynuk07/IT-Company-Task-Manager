from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=63, unique=True)


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        name="worker"
    )


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("LOW", "Low"),
        ("AVERAGE", "Average"),
        ("HIGH", "High"),
        ("URGENT", "Urgent")
    )

    name = models.CharField(max_length=63)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField()
    priority = models.CharField(
        max_length=12,
        choices=PRIORITY_CHOICES,
        default="LOW"
    )

    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, name="task")
    assignees = models.ManyToManyField(Worker, name="task")
