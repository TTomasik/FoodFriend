from django import forms
from foodfriend.models import UserExtend, Meal, Food, Days, MEALS, Quantity
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

# class CreateMealForm(ModelForm):
#     foods = forms.ChoiceField(queryset=Food.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
#     quantity = forms.IntegerField()
#     class Meta:
#         model = Meal
#         fields = ('meal_name', 'day', 'foods')
#
#     def __init__(self, *args, **kwargs):
#         super(CreateMealForm, self).__init(*args, **kwargs)
#         self.fields['extra_field'].initial = "harvard"

class CreateMealForm(forms.Form):
    day = forms.ModelChoiceField(queryset=Days.objects.all(), required=True, empty_label="Choose day:")
    meal = forms.ChoiceField(choices=MEALS, required=True)
    foods1 = forms.ModelChoiceField(queryset=Food.objects.all(), required=True, empty_label="Choose food:")
    quantity1 = forms.IntegerField()
    foods2 = forms.ModelChoiceField(queryset=Food.objects.all(), required=False, empty_label="Choose food:")
    quantity2 = forms.IntegerField(required=False)
    foods3 = forms.ModelChoiceField(queryset=Food.objects.all(), required=False, empty_label="Choose food:")
    quantity3 = forms.IntegerField(required=False)
    foods4 = forms.ModelChoiceField(queryset=Food.objects.all(), required=False, empty_label="Choose food:")
    quantity4 = forms.IntegerField(required=False)
    foods5 = forms.ModelChoiceField(queryset=Food.objects.all(), required=False, empty_label="Choose food:")
    quantity5 = forms.IntegerField(required=False)









# class CreateMealForm(ModelForm):
#     class Meta:
#         model = Meal
#         fields = '__all__'







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








