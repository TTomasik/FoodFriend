from django.contrib import admin
from foodfriend.models import UserExtend, Food, Meal, Days, Quantity, MEALS




@admin.register(UserExtend)
class UserExtendAdmin(admin.ModelAdmin):

    list_display = ('user', 'image_url', 'age', 'sex', 'weight', 'height', 'creation_date')

    def image_url(self, obj):
        return "<img src ='/{}' width='50' height='50' >".format(obj.avatar)

    image_url.allow_tags = True

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'grams', 'kcal', 'proteins', 'carbs', 'fats')
    # inlines = ('QuantityInline', )

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('meal_name', 'Foods')
    # inlines = ('QuantityInline', )

    def Foods(self, meal_food):
        return ",  ".join([str(t) for t in meal_food.foods.all()])

@admin.register(Days)
class DayAdmin(admin.ModelAdmin):
    list_display = ('date', 'date_user','day_calories', 'day_proteins', 'day_carbs', 'day_fats')

@admin.register(Quantity)
class QuantityAdmin(admin.ModelAdmin):
    # meal_quantity = dict(MEALS).get(meal.meal_name)
    list_display = ('meal_quantity', 'food_quantity', 'quantity', 'kcal_quant', 'proteins_quant', 'carbs_quant', 'fats_quant')


class QuantityInline(admin.TabularInline):
    model = Quantity
    extra = 1






