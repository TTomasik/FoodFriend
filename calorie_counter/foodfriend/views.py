from django.shortcuts import render
from foodfriend.forms import LoginForm, UserExtendForm, CreateAccountForm, CreateMealForm, CreateMealForm2, Calendar, WaterForm, DeleteWaterForm
from foodfriend.models import UserExtend, TARGETS, SEX, Days, Meal, Food, MEALS, Quantity
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
import datetime
import math
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
import calendar
from datetime import timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from foodfriend.serializers import FoodSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView


class Index(View):
    def get(self, request):
        return redirect('/index')

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

        if user is not None and User.objects.filter(username__iexact=u).exists():
            login(request, user)
            return redirect("/index")
        else:
            return HttpResponse("""<body bgcolor=#5A5A29><h1><center><br><br><br><br><font color='white'>
            Incorrect login or password :(<br><br><img src='/static/foodfriend/img/rotten.gif'><center>
            </font></h1></body>""")
        # przekierowanie dalej
        # else:
        #     # return render(request, "exercises/login.html", {"form": form})
        #     return HttpResponse("<h1>Nieprawidłowy login lub hasło.</h1>")

# LoginRequiredMixin, UserPassesTestMixin,  <--- tego uzywac do ponizszego w class MyInfo

class MyInfo(LoginRequiredMixin, View):
    def get(self, request, my_id):
        if not self.request.user.is_superuser:
            my_id = self.request.user.id
        cont = {}
        extended = UserExtend.objects.get(user_id=my_id)
        user = User.objects.get(pk=my_id)
        cont['my_id'] = extended.user_id
        cont['avatar'] = extended.avatar
        cont['user'] = user.username
        cont['age'] = extended.age
        cont['sex'] = dict(SEX).get(extended.sex)
        cont['weight'] = extended.weight
        cont['height'] = extended.height
        cont['target'] = dict(TARGETS).get(extended.target)
        cont['calories'] = extended.calories

        return render(request, "foodfriend/myinfo.html", cont)

    def post(self, request, my_id):
        if not self.request.user.is_superuser:
            my_id = self.request.user.id
        return redirect('/myinfo/{}'.format(my_id))



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
                if len(User.objects.filter(username=user)) > 0:
                    return HttpResponse("""<body bgcolor=#5A5A29><h1><center><br><br><br><br><font color='white'>
                        We are sorry but username: {} is already taken :(<br><br><img src='/static/foodfriend/img/rotten.gif'>
                        <center></font></h1></body>""".format(user))
                if len(User.objects.filter(email=em)) > 0:
                    return HttpResponse("""<body bgcolor=#5A5A29><h1><center><br><br><br><br><font color='white'>
                        We are sorry but email: {} is already taken :(<br><br><img src='/static/foodfriend/img/rotten.gif'>
                        <center></font></h1></body>""".format(em))
                else:
                    a = User.objects.create_user(username = user, password = pass1, email = em)
                    a.save()
                    b = UserExtend.objects.create(user = User.objects.get(username=a.username))
                    b.save()
            else:
                return HttpResponse("""<body bgcolor=#5A5A29><h1><center><br><br><br><br><font color='white'>
                        Your password is incorrect :(<br><br><img src='/static/foodfriend/img/rotten.gif'>
                        <center></font></h1></body>""")

        return redirect("/login")

class DaysView(LoginRequiredMixin, View):
    def get(self, request, my_id):
        if not self.request.user.is_superuser:
            my_id = self.request.user.id

        cont = {}
        extended = UserExtend.objects.get(user_id=my_id)
        days = Days.objects.filter(date_user=extended)
        print(days)
        days_list = []
        for day in days:
            d = {}
            d['date'] = day.date
            d['name'] = day.name = calendar.day_name[day.date.weekday()]
            d['id'] = day.id
            days_list.append(d)
        cont['days'] = days_list
        cont['my_id'] = my_id
        cont['avatar'] = extended.avatar
        c = calendar.TextCalendar(calendar.SUNDAY)
        str = c.formatmonth(datetime.date.today().year, datetime.date.today().month)
        cont['pycal'] = str
        cont['cal_month'] = calendar.month_name[datetime.date.today().month]
        cont['cal_day'] = calendar.day_name[datetime.datetime.today().weekday()]
        cont['cal_year'] = datetime.date.today().year
        week1 = []
        week_1 = []
        week_1_yes_no = []
        week2 = []
        week_2 = []
        week_2_yes_no = []
        week3 = []
        week_3 = []
        week_3_yes_no = []
        week4 = []
        week_4 = []
        week_4_yes_no = []
        week5 = []
        week_5 = []
        week_5_yes_no = []
        user_days = [i['date'] for i in days_list]
        print(user_days)
        for index, i in enumerate(c.itermonthdates(datetime.date.today().year, datetime.date.today().month)):
            if index in range (0, 7):
                if i in user_days:
                    week1.append(i)
                    week_1_yes_no.append("yes")
                    week_1.append(i.day)
                if i not in user_days:
                    week1.append(i)
                    week_1_yes_no.append("not")
                    week_1.append(i.day)
            if index in range (7, 14):
                if i in user_days:
                    week2.append(i)
                    week_2_yes_no.append("yes")
                    week_2.append(i.day)
                if i not in user_days:
                    week2.append(i)
                    week_2_yes_no.append("not")
                    week_2.append(i.day)
            if index in range (14, 21):
                if i in user_days:
                    week3.append(i)
                    week_3_yes_no.append("yes")
                    week_3.append(i.day)
                if i not in user_days:
                    week3.append(i)
                    week_3_yes_no.append("not")
                    week_3.append(i.day)
            if index in range (21, 28):
                if i in user_days:
                    week4.append(i)
                    week_4_yes_no.append("yes")
                    week_4.append(i.day)
                if i not in user_days:
                    week4.append(i)
                    week_4_yes_no.append("not")
                    week_4.append(i.day)
            if index in range (28, 35):
                if i in user_days:
                    week5.append(i)
                    week_5_yes_no.append("yes")
                    week_5.append(i.day)
                if i not in user_days:
                    week5.append(i)
                    week_5_yes_no.append("not")
                    week_5.append(i.day)
        week_1_id = []
        week_2_id = []
        week_3_id = []
        week_4_id = []
        week_5_id = []
        for i in week1:
            if i in user_days:
                week_1_id.append(Days.objects.filter(date_user=extended, date=i)[0].id)
            if i not in user_days:
                week_1_id.append(False)
        for i in week2:
            if i in user_days:
                week_2_id.append(Days.objects.filter(date_user=extended, date=i)[0].id)
            if i not in user_days:
                week_2_id.append(False)
        for i in week3:
            if i in user_days:
                week_3_id.append(Days.objects.filter(date_user=extended, date=i)[0].id)
            if i not in user_days:
                week_3_id.append(False)
        for i in week4:
            if i in user_days:
                week_4_id.append(Days.objects.filter(date_user=extended, date=i)[0].id)
            if i not in user_days:
                week_4_id.append(False)
        for i in week5:
            if i in user_days:
                week_5_id.append(Days.objects.filter(date_user=extended, date=i)[0].id)
            if i not in user_days:
                week_5_id.append(False)
        cont['week_1'] = week_1
        cont['week_2'] = week_2
        cont['week_3'] = week_3
        cont['week_4'] = week_4
        cont['week_5'] = week_5
        cont['cal_month_number'] = datetime.date.today().month-1
        cont['no'] = ["not"]
        cont['yes'] = ['yes']
        cont['week_1_with_yes_no'] = zip(week_1_yes_no, week_1, week_1_id)
        cont['week_2_with_yes_no'] = zip(week_2_yes_no, week_2, week_2_id)
        cont['week_3_with_yes_no'] = zip(week_3_yes_no, week_3, week_3_id)
        cont['week_4_with_yes_no'] = zip(week_4_yes_no, week_4, week_4_id)
        cont['week_5_with_yes_no'] = zip(week_5_yes_no, week_5, week_5_id)
        print(week_4)
        print(week_4_id)
        print(week4)
        return render(request, "foodfriend/calendar.html", cont)


class MealsView(LoginRequiredMixin, View):
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
        cont['avatar'] = user.userextend.avatar


        return render(request, "foodfriend/meal.html", cont)

class FoodsView(LoginRequiredMixin, View):
    def get(self, request, my_id, day_id, meal_id):
        if not self.request.user.is_superuser:
            my_id = self.request.user.id

        cont = {}
        day = Days.objects.get(pk=day_id)
        user = User.objects.get(pk=my_id)
        meal = Meal.objects.get(pk=meal_id)
        extended = UserExtend.objects.get(user_id=my_id)
        foods = meal.foods.all()
        food_list = []
        kcal_sum = []
        proteins_sum = []
        carbs_sum = []
        fats_sum = []
        for food in foods:
            quant = Quantity.objects.filter(food_quantity__id=food.id, meal_quantity__id=meal_id)[0].quantity

            d = {}
            if food.id == 53:
                pass
            else:
                d['id'] = food.id
                d['name'] = food.name
                d['kcal'] = food.kcal = round(food.kcal*quant/food.grams, 0)
                d['proteins'] = food.proteins = round(food.proteins*quant/food.grams, 0)
                d['carbs'] = food.carbs = round(food.carbs*quant/food.grams, 0)
                d['fats'] = food.fats = round(food.fats*quant/food.grams, 0)
                d['grams'] = food.grams
                d['quantity'] = quant
                print(quant)
                kcal_sum.append(food.kcal)
                proteins_sum.append(food.proteins)
                carbs_sum.append(food.carbs)
                fats_sum.append(food.fats)
                food_list.append(d)

        cont['food_names'] = food_list
        cont['my_id'] = my_id
        cont['meal_id'] = meal.id
        cont['meal_name'] = dict(MEALS).get(meal.meal_name)
        cont['day_date'] = day.date
        cont['day_id'] = day.id
        cont['avatar'] = extended.avatar
        cont['kcal_sum'] = sum(kcal_sum)
        cont['proteins_sum'] = sum(proteins_sum)
        cont['carbs_sum'] = sum(carbs_sum)
        cont['fats_sum'] = sum(fats_sum)
        cont['zero'] = [0.0]


        return render(request, "foodfriend/food.html", cont)

    def post(self, request, my_id, day_id, meal_id):
        my_id = self.request.user.id
        cont={}
        day = Days.objects.get(pk=day_id)
        user = User.objects.get(pk=my_id)
        meal = Meal.objects.get(pk=meal_id)
        cont['day_id'] = day.id
        cont['my_id'] = my_id
        cont['meal_id'] = meal.id
        result = []
        if "csrfmiddlewaretoken" in request.POST:
            result = [s for s in request.POST if s.isdigit()]

        food_id = int(result[0])
        print(result[0])
        to_change = Quantity.objects.filter(food_quantity__id=food_id, meal_quantity__id=meal_id)[0]
        to_change.quantity = 0.0
        to_change.save()
        return redirect('/calendar/{}/meal/{}/food/{}'.format(my_id, day_id, meal_id))

class CreateMealTwo(LoginRequiredMixin, View):

    def get(self, request, meal_id):
        print(meal_id)
        meal_type = Meal.objects.filter(id=meal_id)[0].meal_name
        my_id = self.request.user.id
        user = User.objects.get(pk=my_id)
        today = Days.objects.filter(date_user=request.user.userextend, date=datetime.date.today())[0]
        today_meals = Meal.objects.filter(day__date_user=user.userextend, day__date=datetime.date.today())
        if len(today_meals) == 0:
            a = 0
        if len(today_meals) == 1:
            a = 1
        if len(today_meals) == 2:
            a = 2
        if len(today_meals) == 3:
            a = 3
        if len(today_meals) == 4:
            a = 4
        if len(today_meals) == 5:
            a = 4
        form = CreateMealForm(initial = {"meal": meal_type, "day": today})
        form.fields["day"].queryset = Days.objects.filter(date_user=user.userextend)
        avatar = user.userextend.avatar

        return render(request, "foodfriend/meal_form.html", {"form": form, "avatar": avatar})

    def post(self, request, meal_id):
        form = CreateMealForm(request.POST)
        my_id = self.request.user.id

        if form.is_valid():
            name = form.cleaned_data['meal']
            day = form.cleaned_data['day']
            food1 = form.cleaned_data['foods1']
            quantity1 = form.cleaned_data['quantity1']
            food2 = form.cleaned_data['foods2']
            quantity2 = form.cleaned_data['quantity2']
            food3 = form.cleaned_data['foods3']
            quantity3 = form.cleaned_data['quantity3']
            food4 = form.cleaned_data['foods4']
            quantity4 = form.cleaned_data['quantity4']
            food5 = form.cleaned_data['foods5']
            quantity5 = form.cleaned_data['quantity5']
            print(quantity1)


            meal, _create = Meal.objects.get_or_create(meal_name = name, day = day)
            day_foods_list = meal.foods.all()

            if food1 not in day_foods_list:
                Quantity.objects.create(meal_quantity=meal, food_quantity=food1, quantity=abs(quantity1))
            else:
                Quantity.objects.filter(meal_quantity=meal, food_quantity=food1).update(quantity=abs(quantity1))

            if food2 != None and quantity2 != None:
                if food2 not in day_foods_list:
                    Quantity.objects.create(meal_quantity=meal, food_quantity=food2, quantity=abs(quantity2))
                else:
                    Quantity.objects.filter(meal_quantity=meal, food_quantity=food2).update(quantity=abs(quantity2))
            else:
                pass
            if food3 != None and quantity3 != None:
                if food3 not in day_foods_list:
                    Quantity.objects.create(meal_quantity=meal, food_quantity=food3, quantity=abs(quantity3))
                else:
                    Quantity.objects.filter(meal_quantity=meal, food_quantity=food3).update(quantity=abs(quantity3))
            else:
                pass
            if food4 != None and quantity4 != None:
                if food4 not in day_foods_list:
                    Quantity.objects.create(meal_quantity=meal, food_quantity=food4, quantity=abs(quantity4))
                else:
                    Quantity.objects.filter(meal_quantity=meal, food_quantity=food4).update(quantity=abs(quantity4))
            else:
                pass
            if food5 != None and quantity5 != None:
                if food5 not in day_foods_list:
                    Quantity.objects.create(meal_quantity=meal, food_quantity=food5, quantity=abs(quantity5))
                else:
                    Quantity.objects.filter(meal_quantity=meal, food_quantity=food5).update(quantity=abs(quantity5))
            else:
                pass

        return redirect('/calendar/{}/meal/{}/food/{}'.format(my_id, day.id, meal.id))


class CreateMeal(LoginRequiredMixin, View):

    def get(self, request):
        my_id = self.request.user.id
        user = User.objects.get(pk=my_id)
        today = Days.objects.filter(date_user=request.user.userextend, date=datetime.date.today())[0]
        today_meals = Meal.objects.filter(day__date_user=user.userextend, day__date=datetime.date.today())
        if len(today_meals) == 0:
            a = 0
        if len(today_meals) == 1:
            a = 1
        if len(today_meals) == 2:
            a = 2
        if len(today_meals) == 3:
            a = 3
        if len(today_meals) == 4:
            a = 4
        if len(today_meals) == 5:
            a = 4
        form = CreateMealForm(initial = {"meal": MEALS[a][0], "day": today})
        form.fields["day"].queryset = Days.objects.filter(date_user=user.userextend)
        avatar = user.userextend.avatar

        return render(request, "foodfriend/meal_form.html", {"form": form, "avatar": avatar})

    def post(self, request):
        form = CreateMealForm(request.POST)
        my_id = self.request.user.id

        if form.is_valid():
            name = form.cleaned_data['meal']
            day = form.cleaned_data['day']
            food1 = form.cleaned_data['foods1']
            quantity1 = form.cleaned_data['quantity1']
            food2 = form.cleaned_data['foods2']
            quantity2 = form.cleaned_data['quantity2']
            food3 = form.cleaned_data['foods3']
            quantity3 = form.cleaned_data['quantity3']
            food4 = form.cleaned_data['foods4']
            quantity4 = form.cleaned_data['quantity4']
            food5 = form.cleaned_data['foods5']
            quantity5 = form.cleaned_data['quantity5']


            meal, _create = Meal.objects.get_or_create(meal_name = name, day = day)
            day_foods_list = meal.foods.all()

            if food1 not in day_foods_list:
                Quantity.objects.create(meal_quantity=meal, food_quantity=food1, quantity=quantity1)
            else:
                Quantity.objects.filter(meal_quantity=meal, food_quantity=food1).update(quantity=quantity1)

            if food2 != None and quantity2 != None:
                if food2 not in day_foods_list:
                    Quantity.objects.create(meal_quantity=meal, food_quantity=food2, quantity=quantity2)
                else:
                    Quantity.objects.filter(meal_quantity=meal, food_quantity=food2).update(quantity=quantity2)
            else:
                pass
            if food3 != None and quantity3 != None:
                if food3 not in day_foods_list:
                    Quantity.objects.create(meal_quantity=meal, food_quantity=food3, quantity=quantity3)
                else:
                    Quantity.objects.filter(meal_quantity=meal, food_quantity=food3).update(quantity=quantity3)
            else:
                pass
            if food4 != None and quantity4 != None:
                if food4 not in day_foods_list:
                    Quantity.objects.create(meal_quantity=meal, food_quantity=food4, quantity=quantity4)
                else:
                    Quantity.objects.filter(meal_quantity=meal, food_quantity=food4).update(quantity=quantity4)
            else:
                pass
            if food5 != None and quantity5 != None:
                if food5 not in day_foods_list:
                    Quantity.objects.create(meal_quantity=meal, food_quantity=food5, quantity=quantity5)
                else:
                    Quantity.objects.filter(meal_quantity=meal, food_quantity=food5).update(quantity=quantity5)
            else:
                pass

            # else:
            #     # meal.foods.set(food)
            #     Quantity.objects.create(meal_quantity=meal, food_quantity=food1, quantity=quantity1)
            #     if food2 != None and quantity2 != None:
            #         Quantity.objects.create(meal_quantity=meal, food_quantity=food2, quantity=quantity2)
            #     else:
            #         pass
            #     if food3 != None and quantity3 != None:
            #         Quantity.objects.create(meal_quantity=meal, food_quantity=food3, quantity=quantity3)
            #     else:
            #         pass
            #     if food4 != None and quantity4 != None:
            #         Quantity.objects.create(meal_quantity=meal, food_quantity=food4, quantity=quantity4)
            #     else:
            #         pass
            #     if food5 != None and quantity5 != None:
            #         Quantity.objects.create(meal_quantity=meal, food_quantity=food5, quantity=quantity5)
            #     else:
            #         pass

                # meal = Meal.objects.create(meal_name = name, day = day, foods=food)
                # meal.save()

        return redirect('/calendar/{}/meal/{}/food/{}'.format(my_id, day.id, meal.id))

# class AddDay(View):
#     def get(self, request, my_id):
#         try:
#             my_id = self.request.user.id
#             user_extend = UserExtend.objects.get(user_id=my_id)
#             day = Days.objects.create(date_user=user_extend)
#             day.save()
#             return redirect('/calendar/{}'.format(my_id))
#         except IntegrityError:
#             return HttpResponse('<h1>You have already done this <b>today</b>!</h1>')

class UpdateMeal2(View):
    def get(self, request, meal_id):
        p = Meal.objects.get(pk=meal_id)
        form = CreateMealForm2(instance=p)
        cont = {}
        food_quant = []
        for food in form:
            d = {}
            print(food)
            quant = Quantity.objects.filter(meal_quantity=Meal.objects.get(pk=meal_id), food_quantity=Food.objects.get(pk=11))
            d['quantity'] = food.quantity = quant
            food_quant.append(d)

        cont['food_quants'] = food_quant

        return render(request, "foodfriend/meal_form2.html", {"form": form}, cont)

    def post(self, request, meal_id):
        p = Meal.objects.get(pk=meal_id)
        form = CreateMealForm2(request.POST, instance=p)
        if form.is_valid():
            form.save()
        return render(request, "foodfriend/meal_form2.html", {"form": form})



class UpdateMeal(UpdateView):
    def get_success_url(self, **kwargs):
        return reverse('update-meal', kwargs={'meal_id':self.object.id,
                                                'my_id':self.object.day.date_user.id,
                                                'day_id':self.object.day.id})
    model = Meal
    fields = ['foods']
    template_name_suffix = '_form'

# class UpdateMeal(View):
#
#     def get(self, request, my_id, day_id, meal_id):
#         if not self.request.user.is_superuser:
#             my_id = self.request.user.id
#
#         day = Days.objects.get(pk=day_id)
#         user = User.objects.get(pk=my_id)
#         meal = Meal.objects.get(pk=meal_id)
#
#         form = CreateMealForm(request.POST)
#         return render(request, "foodfriend/meal_form.html", {"form": form}, day_id, my_id, meal_id)

###trzeba to usunac bo tylko zasmieca
class UpdateUser(LoginRequiredMixin, UpdateView):
    def get_success_url(self, **kwargs):
        return reverse('my-info', kwargs={'my_id':self.object.user_id})

    model = UserExtend
    fields = ['avatar', 'age', 'sex', 'weight', 'height', 'factor', 'target']

    template_name_suffix = '_update_form'

class CreateFood(LoginRequiredMixin, CreateView):
    def get_success_url(self, **kwargs):
        return reverse('food-list')

    model = Food
    fields = '__all__'
    template_name_suffix = '_form'
    success_url = '/foodlist'

class FoodList(LoginRequiredMixin, View):
    def get(self, request):
        extended = UserExtend.objects.get(user_id=self.request.user.id)
        cont = {}
        foods = Food.objects.all()
        food_list = []
        for m in foods:
            d = {}
            d['name'] = m.name
            d['kcal'] = m.kcal
            d['protein'] = m.proteins
            d['carbs'] = m.carbs
            d['fats'] = m.fats
            d['grams'] = m.grams
            food_list.append(d)
        cont['food'] = food_list
        cont['avatar'] = extended.avatar

        return render(request, 'foodfriend/food_list.html', cont)

class UserMacros(LoginRequiredMixin, View):
    def get(self, request, my_id=None):
        if not my_id:
            my_id = self.request.user.id
            day, _create = Days.objects.get_or_create(date=datetime.date.today(), date_user=request.user.userextend)
        extended = UserExtend.objects.get(user_id=my_id)
        cont = {}
        cont['calories'] = round(day.day_calories, 1)
        cont['proteins'] = round(day.day_proteins, 1)
        cont['carbs'] = round(day.day_carbs, 1)
        cont['fats'] = round(day.day_fats, 1)
        cont['avatar'] = extended.avatar
        if extended.calories == None:
            cont['water'] = 0
            cont['progress'] = 0
        else:
            cont['water'] = int(day.day_water)
            cont['progress'] = round(day.day_water / extended.water, 1) * 100

        form = WaterForm()
        form2 = DeleteWaterForm()

        return render(request, 'foodfriend/index.html', cont, {"form": form})

    def post(self, request):
        form = WaterForm(request.POST)
        my_id = self.request.user.id
        user = User.objects.get(pk=my_id)
        today = Days.objects.filter(date_user=request.user.userextend, date=datetime.date.today())[0]
        if form.is_valid():
            if 'add_water' in request.POST:
                meal, _create = Meal.objects.get_or_create(meal_name=1, day=today)
                # for i in Quantity.objects.filter(meal_quantity=meal, food_quantity__id=53):
                #     before += i.quantity
                # water_sum = int(water+before)
                Quantity.objects.create(meal_quantity=meal, food_quantity_id=53, quantity=250)
                return redirect('/index')
            if 'delete_water' in request.POST:
                meal, _create = Meal.objects.get_or_create(meal_name=1, day=today)
                to_delete = Quantity.objects.filter(meal_quantity=meal, food_quantity__id=53)[::-1][0]
                to_delete.delete()
                return redirect('/index')






    # if not my_id:
    #     my_id = self.request.user.id
    #     extended = UserExtend.objects.get(pk=my_id)
    #     days = Days.objects.filter(date_user=extended)
    #     for d in days:
    #         if d.date == datetime.date.today():
    #             pass
    #         else:
    #             day = Days.objects.create(date_user=request.user.userextend)
    #             day.save()
    #
    #     day = Days.objects.get(date=datetime.date.today(), date_user=request.user.userextend)

class MyPerson(LoginRequiredMixin, View):
    def get(self, request, my_id):
        p = UserExtend.objects.get(user_id=my_id)
        form = UserExtendForm(instance=p)
        avatar = p.avatar
        return render(request, "foodfriend/userextend_update_form2.html", {"form": form, "avatar": avatar})


    def post(self, request, my_id):
        p = UserExtend.objects.get(user_id=my_id)
        form = UserExtendForm(request.POST, request.FILES, instance=p)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/myinfo/{}'.format(my_id))


# Quantity.objects.filter(meal_quantity__day__date=datetime.date.today())
# Quantity.objects.filter(meal_quantity__day__date=datetime.date.today(), meal_quantity__day__date_user=user.userextend)




class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        if not self.request.user.is_superuser:
            my_id = self.request.user.id

        cont = []
        extended = UserExtend.objects.get(user_id=self.request.user.id)
        days = Days.objects.filter(date_user=extended)

        for d in days:
            cont.append(d.date)
        day = datetime.date.today()

        if len(days) < 2:
            return cont[datetime.date.today(), "Tomorrow"]
        labels = cont[-7::]
        return labels

    def get_data(self):
        if not self.request.user.is_superuser:
            my_id = self.request.user.id

        cont = []
        extended = UserExtend.objects.get(user_id=my_id)
        days = Days.objects.filter(date_user=extended)
        for d in days:
            cont.append(d)

        days_final = cont[-7::]
        kcals = []
        proteins = []
        carbs = []
        fats = []
        for day in days_final:
            kcal = round(day.day_calories, 1)
            kcals.append(kcal)
            prot = round(day.day_proteins, 1)
            proteins.append(prot)
            carb = round(day.day_carbs, 1)
            carbs.append(carb)
            fat = round(day.day_fats, 1)
            fats.append(fat)
        user_calories = []
        for i in range(7):
            user_calories.append(extended.calories)

        if len(kcals) < 2:
            kcals = [0, 0]
            proteins = [0, 0]
            carbs = [0, 0]
            fats = [0, 0]
            user_calories = [extended.calories, extended.calories]


        return user_calories, kcals, proteins, carbs, fats


line_chart = TemplateView.as_view(template_name='foodfriend/line_chart.html')
line_chart_json = LineChartJSONView.as_view()

class DatePicker(View):
    def get(self, request):
        if not self.request.user.is_superuser:
            my_id = self.request.user.id
        user = User.objects.get(pk=self.request.user.id)
        form = Calendar()
        form.fields["cal"].queryset = Days.objects.filter(date_user=user.userextend)
        return render(request, "foodfriend/date_picker.html", {'form': form})

date_picker = TemplateView.as_view(template_name="foodfriend/date_picker.html")
date_picker_jquery = DatePicker.as_view()


class FoodListSerializer(APIView):
    def get(self, request, format=None):
        food = Food.objects.all()
        serializer = FoodSerializer(food, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FoodSerializerDetails(APIView):
    def get_object(self, pk):
        try:
            return Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        detail = self.get_object(pk)
        serializer = FoodSerializer(detail, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        food_put = self.get_object(pk)
        serializer = FoodSerializer(food_put, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        food = self.get_object(pk)
        food.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# from requests.auth import HTTPBasicAuth
#     food = requests.get('http://127.0.0.1:8000/food_list_serializer/?format=json',
#                         auth=HTTPBasicAuth('user', 'pass'))


