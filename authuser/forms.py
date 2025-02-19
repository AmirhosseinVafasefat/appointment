from authuser.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator


class RegistrationForm(UserCreationForm):
    phone_number = forms.RegexField(
        label='', max_length=30, regex=r"^09[0-9]{9}$",
        help_text="",
        error_messages={'invalid': "شماره تلفن خود را به درستی وارد کنید. مثلا 09011111111",
                        'unique': "این شماره تلفن قبلا وارد شده است.",
                        },
        widget=forms.TextInput(attrs={'class': 'form-control',
                                    'required': 'true',
                                    'placeholder': 'شماره تلفن'
        })
    )

    password1 = forms.CharField(
            label="",
            required=True,
            strip=False,
            widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                    'class': 'form-control',
                                    'required': 'true',
                                    'placeholder': 'رمز'}),
            help_text="",
    )
    password2 = forms.CharField(
            label="",
            required=True,
            widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                    'class': 'form-control',
                                    'required': 'true',
                                    'placeholder': 'تکرار رمز'}),
            strip=False,
            help_text="",
    )

    name = forms.CharField(
         label="",
         required=True,
         widget=forms.PasswordInput(attrs={'class': 'form-control',
                                    'required': 'true',
                                    'placeholder': 'نام'}),
    )

    last_name = forms.CharField(
         label="",
         required=True,
         widget=forms.PasswordInput(attrs={'class': 'form-control',
                                    'required': 'true',
                                    'placeholder': 'نام خانوادگی'}),
    )

    error_messages = {
        'password_mismatch': "تکرار رمز با رمز مطابقت ندارد.",
        'password_too_common': "رمز شما بیش از حد رایج است.",
        'password_too_short': "رمز وارد شده کوتاه است.",
        'password_is_numeric': "رمز وارد شده تماما عدد است."
    }

    class Meta:
            model = User
            fields = ['name', 'last_name', 'phone_number', 'password1', 'password2']

class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11,
                                    validators=[RegexValidator(r'^09[0-9]{9}$')],
                                    label="",
                                    widget=forms.TextInput(attrs={
                                            'class': 'form-control',
                                            'required': 'true',
                                            'placeholder': 'شماره تلفن'
                                            })
    )
    password = forms.CharField(max_length=30,
                               label="",
                               widget=forms.PasswordInput(attrs={
                                            'class': 'form-control',
                                            'required': 'true',
                                            'placeholder': 'رمز'
                                            })
    )
    