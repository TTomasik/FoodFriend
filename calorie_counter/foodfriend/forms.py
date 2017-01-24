from django import forms
from foodfriend.models import UserExtend, Meal, Food, Days, MEALS
from django.core.exceptions import ValidationError
from django.forms import ModelForm, HiddenInput, IntegerField, CharField


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

class UserExtendForm(ModelForm):
    class Meta:
        model = UserExtend
        fields = ('avatar', 'user', 'age', 'sex', 'weight', 'height', 'target')



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

# class CreateMealForm(ModelForm):
#
#     meal_name_quantity = CharField(widget=HiddenInput())
#     food_name_quantity = CharField(widget=HiddenInput())
#
#     class Meta:
#         model = Meal
#         exclude = ['foods',]
#
#     def save(self, commit=True):
#         meal = super(CreateMealForm, self).save()
#         meal_name_quant = Meal.objects.get(name=meal_name_quantity)
#         food = Food.objects.get(name=food_name_quantity)
#         quantity = self.cleaned_data.get('quantity')
#         Quantity.objects.create(quantity=quantity, meal_quantity=meal_name_quant, food_quantity=food)
#
#         return meal








