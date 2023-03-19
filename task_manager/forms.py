from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class WorkerCreateForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "position"
        )
