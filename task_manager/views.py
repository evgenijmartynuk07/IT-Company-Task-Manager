from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from task_manager.models import Task


def index(request):
    tasks = Task.objects.all()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "tasks": tasks,
        "num_visits": num_visits + 1,
    }

    return render(request, "task_manager/index.html", context=context)
