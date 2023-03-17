from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from task_manager.models import Task


def index(request):
    num_task = Task.objects.all().count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_task": num_task,
        "num_visits": num_visits + 1,
    }

    return render(request, "task_manager/index.html", context=context)
