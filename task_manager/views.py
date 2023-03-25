import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.core.paginator import Paginator

from task_manager.forms import WorkerCreateForm, TaskCreateForm, TaskCompletedUpdateForm, WorkerUpdateForm, \
    TaskSearchForm, WorkerSearchForm
from task_manager.models import Task


@login_required
def index(request):
    tasks = Task.objects.prefetch_related(
        "assignees"
    ).select_related(
        "owner"
    ).select_related(
        "task_type"
    ).filter(
        assignees=request.user.id
    )

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    paginator = Paginator(tasks, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "num_visits": num_visits + 1,
        "paginator": paginator,
        "page_obj": page_obj,
    }

    return render(request, "task_manager/index.html", context=context)


class WorkerCreateView(generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreateForm
    success_url = reverse_lazy("task_manager:index")


class WorkerUpdateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = WorkerUpdateForm


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")
        context["search_field"] = WorkerSearchForm(initial={
            "username": username
        })

        return context

    def get_queryset(self):
        queryset = get_user_model().objects.prefetch_related(
            "tasks"
        ).select_related(
            "position"
        )
        form = WorkerSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])

        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    queryset = get_user_model().objects.prefetch_related("tasks").select_related("position")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("task_manager:index")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_field"] = TaskSearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self) -> QuerySet:
        queryset = Task.objects.prefetch_related("assignees").select_related("owner")
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = ("name", "description", "deadline", "priority", "task_type", "assignees")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:index")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees").select_related("task_type")
    form_class = TaskCompletedUpdateForm

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()

        if self.object.deadline < datetime.date.today():
            context["valid_data"] = False
        else:
            context["valid_data"] = True
        return context

    def post(self, request, **kwargs):
        self.object = self.get_object()

        if request.POST.get("is_completed") == "1":
            self.object.is_completed = True
            self.object.save()

        if request.POST.get("assignees") == f"{self.request.user.id}":
            self.object.assignees.add(self.request.user.id)
            self.object.save()

        return redirect("task_manager:task-detail", pk=self.object.pk)
