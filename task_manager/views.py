from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

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


class TaskCreateView(generic.CreateView):
    model = Task
    fields = ("name", "description", "deadline", "priority", "task_type")


class TaskUpdateView(generic.UpdateView):
    model = Task
    fields = ("name", "description", "deadline", "priority", "task_type")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:index")


class TaskDetailView(generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees").select_related("task_type")
