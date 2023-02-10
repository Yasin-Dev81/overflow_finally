from django.forms import ModelForm
from .models import InstaUserForCopy


class NewInstaUserForm(ModelForm):
    class Meta:
        model = InstaUserForCopy
        fields = [
            'username',
            'user_pub',
        ]
