"""calorie_counter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from foodfriend.views import CheckLogin, MyInfo, CreateAccount, DaysView,\
    MealsView, FoodsView, CreateMeal, AddDay, UpdateMeal, UpdateUser, CreateFood, FoodList


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', CheckLogin.as_view(), name='login'),
    url(r'^index/logout$', logout_then_login, name='logout'),
    url(r'^myinfo/(?P<my_id>(\d){1,4})$', MyInfo.as_view(), name='my-info'),
    url(r'^myinfoedit/(?P<my_id>(\d){1,4})$', MyInfo.as_view(), name='my-info-edit'),
    url(r'^createaccount/?$', CreateAccount.as_view(), name='create-account'),
    url(r'^calendar/(?P<my_id>(\d){1,4})$', DaysView.as_view(), name='calendar'),
    url(r'^calendar/(?P<my_id>(\d){1,4})/meal/(?P<day_id>(\d){1,4})$', MealsView.as_view(), name='calendar-meal'),
    url(r'^calendar/(?P<my_id>(\d){1,4})/meal/(?P<day_id>(\d){1,4})/food/(?P<meal_id>(\d){1,4})$', FoodsView.as_view(), name='calendar-food'),
    url(r'^createmeal/$', CreateMeal.as_view(), name='create-meal'),
    url(r'^addday/(?P<my_id>(\d){1,4})$', AddDay.as_view(), name='add-day'),
    url(r'^mealupdate/(?P<pk>\d+)/?$', UpdateMeal.as_view(), name='update-meal'),
    url(r'^userupdate/(?P<pk>\d+)/?$', UpdateUser.as_view(), name='update-user'),
    url(r'^createfood/$', CreateFood.as_view(), name='create-food'),
    url(r'^foodlist/$', FoodList.as_view(), name='food-list'),


]
