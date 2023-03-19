from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import WorkerCreateForm, TaskCreateForm
from task_manager.models import Task


@login_required
def index(request):
    tasks = Task.objects.all()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "tasks": tasks,
        "num_visits": num_visits + 1,
    }

    return render(request, "task_manager/index.html", context=context)


class WorkerCreateView(generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreateForm
    success_url = reverse_lazy("task_manager:index")


class WorkerListView(generic.ListView):
    model = get_user_model()
    queryset = get_user_model().objects.prefetch_related(
        "tasks"
    ).select_related(
        "position"
    )


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("task_manager:index")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = ("name", "description", "deadline", "priority", "task_type", "assignees")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:index")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees").select_related("task_type")
