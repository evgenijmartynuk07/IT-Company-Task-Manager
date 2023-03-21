from django.urls import path

from task_manager.views import index, \
    TaskCreateView, \
    TaskUpdateView, TaskDetailView, TaskDeleteView, WorkerCreateView, WorkerDetailView, WorkerListView, TaskListView, WorkerUpdateView

urlpatterns = [
    path("", index, name="index"),
    path("worker/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("worker/", WorkerListView.as_view(), name="worker-list"),
    path("worker/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("worker/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task/", TaskListView.as_view(), name="task-list"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
]

app_name = "task_manager"
