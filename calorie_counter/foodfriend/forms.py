from django import forms
from foodfriend.models import UserExtend, Meal, Food, Days, MEALS
from django.core.exceptions import ValidationError
from django.forms import ModelForm


class LoginForm(forms.Form):
    login = forms.CharField(
        label='Username',
        max_length=64,
        widget=forms.TextInput,
        required=True,
    )
    password = forms.CharField(
        label='Password',
        max_length=64,
        widget=forms.PasswordInput,
        required=True,
    )

class UserExtendForm(forms.Form):
    class Meta:
        model = UserExtend
        fields = ('avatar', 'user', 'age', 'sex', 'weight', 'height', 'target', 'calories')



class CreateAccountForm(forms.Form):
    login = forms.CharField(
        label='Username',
        max_length=64,
        widget=forms.TextInput,
        required=True,
    )
    password = forms.CharField(
        label='Password',
        max_length=64,
        widget=forms.PasswordInput,
        required=True,
    )
    password2 = forms.CharField(
        label='Password',
        max_length=64,
        widget=forms.PasswordInput,
        required=True,

    )
    email = forms.CharField(
        label='Email',
        max_length=64,
        widget=forms.TextInput,
        required=True,
    )

class CreateMealForm(ModelForm):
    class Meta:
        model = Meal
        fields = '__all__'





