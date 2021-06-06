from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .password_validators import validate_password_length
import re
from django.conf import settings
from .models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)
    mobile_number = forms.CharField(label="Mobile Number", max_length=10, min_length=10, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'mobile_number')

    def clean_mobile_number(self):
        """
        If the mobile number is entered then will validate mobile number.
        """
        mobile_no = self.cleaned_data["mobile_number"]
        if mobile_no:
            if re.search(settings._MOBILE_NO_REGEX.encode().decode(), mobile_no):
                return mobile_no
            else:
                raise ValidationError(_("Invalid mobile number."))