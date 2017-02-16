from django import forms
from foodfriend.models import UserExtend, Meal, Food, Days, MEALS, Quantity
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from dal import autocomplete
import datetime


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

class UserExtendForm(forms.ModelForm):
    def image_url(self, obj):
        return "<img src ='/{}' width='50' height='50' >".format(obj.avatar)

    image_url.allow_tags = True

    class Meta:
        model = UserExtend
        fields = ('avatar', 'age', 'sex', 'weight', 'height', 'factor', 'target')



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


class CreateMealForm(forms.Form):
    day = forms.ModelChoiceField(queryset=Days.objects.all(), required=True, empty_label="Choose day: ", widget=autocomplete.Select2)
    meal = forms.ChoiceField(choices=MEALS, required=True, widget=autocomplete.ModelSelect2)
    foods1 = forms.ModelChoiceField(queryset=Food.objects.all(), required=True, empty_label="Choose food:", widget=autocomplete.ModelSelect2)
    quantity1 = forms.FloatField(label='grams')
    foods2 = forms.ModelChoiceField(queryset=Food.objects.all(), required=False, empty_label="Choose food:", widget=autocomplete.ModelSelect2)
    quantity2 = forms.FloatField(label='grams', required=False)
    foods3 = forms.ModelChoiceField(queryset=Food.objects.all(), required=False, empty_label="Choose food:", widget=autocomplete.ModelSelect2)
    quantity3 = forms.FloatField(label='grams', required=False)
    foods4 = forms.ModelChoiceField(queryset=Food.objects.all(), required=False, empty_label="Choose food:", widget=autocomplete.ModelSelect2)
    quantity4 = forms.FloatField(label='grams', required=False)
    foods5 = forms.ModelChoiceField(queryset=Food.objects.all(), required=False, empty_label="Choose food:", widget=autocomplete.ModelSelect2)
    quantity5 = forms.FloatField(label='grams', required=False)




class CreateMealForm2(ModelForm):
    class Meta:
        model = Meal
        fields = ('foods', )





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








