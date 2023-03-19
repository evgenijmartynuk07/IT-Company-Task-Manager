from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class WorkerCreateForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for field_name in ["username", "password1", "password2"]:
            self.fields[field_name].help_text = None

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "position"
        )

