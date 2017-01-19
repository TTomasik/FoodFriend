from django.shortcuts import render
from foodfriend.forms import LoginForm, UserExtendForm, CreateAccountForm, CreateMealForm
from foodfriend.models import UserExtend, TARGETS, SEX, Days, Meal, Food, MEALS
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import UpdateView
from django.urls import reverse_lazy, reverse
from django.db import IntegrityError
from django.http import Http404


class CheckLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "foodfriend/index.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            u = form.cleaned_data['login']
            p = form.cleaned_data['password']
        else:
            return HttpResponse("<h1>Wprowadzone dane są niepoprawne.</h1>")

        user = authenticate(username=u, password=p)
        form = LoginForm()
        # my_id = user.pk

        if user is not None:
            login(request, user)
            return redirect("/index")
        else:
            return HttpResponse("<h1><font color='red'>Incorrect login or password!</font></h1>")
        # przekierowanie dalej
        # else:
        #     # return render(request, "exercises/login.html", {"form": form})
        #     return HttpResponse("<h1>Nieprawidłowy login lub hasło.</h1>")

# LoginRequiredMixin, UserPassesTestMixin,  <--- tego uzywac do ponizszego w class MyInfo

class MyInfo(View):
    def get(self, request, my_id):
        if not self.request.user.is_superuser:
            my_id = self.request.user.id
        cont = {}
        extended = UserExtend.objects.get(pk=my_id)
        user = User.objects.get(pk=my_id)
        cont['my_id'] = user.pk
        cont['avatar'] = extended.avatar
        cont['user'] = user.username
        cont['age'] = extended.age
        cont['sex'] = dict(SEX).get(extended.sex)
        cont['weight'] = extended.weight
        cont['height'] = extended.height
        cont['target'] = dict(TARGETS).get(extended.target)
        cont['calories'] = extended.calories

        return render(request, "foodfriend/myinfo.html", cont)


class CreateAccount(View):
    def get(self, request):
        form = CreateAccountForm()
        return render(request, "foodfriend/user_form.html", {"form": form})

    def post(self, request):
        form = CreateAccountForm(request.POST)
        if form.is_valid():

            user = form.cleaned_data['login']
            pass1 = form.cleaned_data['password']
            pass2 = form.cleaned_data['password2']
            em = form.cleaned_data['email']

            if pass1 == pass2:
                a = User.objects.create_user(username = user, password = pass1, email = em)
                a.save()
                b = UserExtend.objects.create(user = User.objects.get(username=a.username))
                b.save()
            else:
                return HttpResponse("<h1>Wprowadzone hasło jest niepoprawne.</h1>")

        return redirect("/index")

class DaysView(View):
    def get(self, request, my_id):
        if not self.request.user.is_superuser:
            my_id = self.request.user.id

        cont = {}
        extended = UserExtend.objects.get(pk=my_id)
        days = Days.objects.filter(date_user=extended)
        days_list = []
        for day in days:
            d = {}
            d['date'] = day.date
            d['id'] = day.id
            days_list.append(d)
        cont['days'] = days_list
        cont['my_id'] = my_id

        return render(request, "foodfriend/calendar.html", cont)


class MealsView(View):
    def get(self, request, my_id, day_id):
        if not self.request.user.is_superuser:
            my_id = self.request.user.id

        cont = {}
        day = Days.objects.get(pk=day_id)
        user = User.objects.get(pk=my_id)
        meals = Meal.objects.filter(day__date_user=user.userextend, day__date=day.date)
        meal_list = []
        for meal in meals:
            d = {}
            d['name'] = dict(MEALS).get(meal.meal_name)
            d['id'] = meal.id
            d['day_id'] = day.id
            meal_list.append(d)
        cont['meal_names'] = meal_list
        cont['my_id'] = my_id
        cont['day_id'] = day.id
        cont['day_date'] = day.date


        return render(request, "foodfriend/meal.html", cont)

class FoodsView(View):
    def get(self, request, my_id, day_id, meal_id):
        if not self.request.user.is_superuser:
            my_id = self.request.user.id

        cont = {}
        day = Days.objects.get(pk=day_id)
        user = User.objects.get(pk=my_id)
        meal = Meal.objects.get(pk=meal_id)
        foods = meal.foods.all()
        food_list = []
        for food in foods:
            d = {}
            d['name'] = food.name
            d['kcal'] = food.kcal
            d['proteins'] = food.proteins
            d['carbs'] = food.carbs
            d['fats'] = food.fats
            d['grams'] = food.grams
            food_list.append(d)
        cont['food_names'] = food_list
        cont['my_id'] = my_id
        cont['meal_id'] = meal.id

        return render(request, "foodfriend/food.html", cont)


class CreateMeal(View):

    def get(self, request):
        my_id = self.request.user.id
        user = User.objects.get(pk=my_id)
        form = CreateMealForm()
        form.fields["day"].queryset = Days.objects.filter(date_user=user.userextend)
        return render(request, "foodfriend/meal_form.html", {"form": form})

    def post(self, request):
        form = CreateMealForm(request.POST)
        my_id = self.request.user.id

        if form.is_valid():

            name = form.cleaned_data['meal_name']
            day = form.cleaned_data['day']
            food = form.cleaned_data['foods']

            meal, _create = Meal.objects.get_or_create(meal_name = name, day = day)
            print(_create)
            if _create is False:
                return HttpResponse("""<h1>You have already added this meal today!</h1>
                <h1><a href="/calendar/{}">Create another meal or update exist one!</a></h1>
                """.format(my_id))
            else:
                print(meal)
                meal.foods.set(food)
                # meal = Meal.objects.create(meal_name = name, day = day, foods=food)
                # meal.save()

        return redirect('/calendar/{}'.format(my_id))

class AddDay(View):
    def get(self, request, my_id):
        try:
            my_id = self.request.user.id
            user_extend = UserExtend.objects.get(pk=my_id)
            day = Days.objects.create(date_user=user_extend)
            day.save()
            return redirect('/calendar/{}'.format(my_id))
        except IntegrityError:
            return HttpResponse('<h1>You have already done this <b>today</b>!</h1>')

class UpdateMeal(UpdateView):
    def get_success_url(self, **kwargs):
        return reverse('calendar-food', kwargs={'meal_id':self.object.id,
                                                'my_id':self.object.day.date_user.id,
                                                'day_id':self.object.day.id})
    model = Meal
    fields = ['foods']
    template_name_suffix = '_form'


class UpdateUser(UpdateView):
    def get_success_url(self, **kwargs):
        return reverse('my-info', kwargs={'my_id':self.object.id})

    model = UserExtend
    fields = ['avatar', 'age', 'sex', 'weight', 'height', 'factor', 'target']

    template_name_suffix = '_update_form'







