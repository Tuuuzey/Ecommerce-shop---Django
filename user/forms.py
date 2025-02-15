from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm

class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
        