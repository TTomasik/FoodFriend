from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import math

TARGETS = (
    (0, "Choose your target:"),
    (1, "Build muscle"),
    (2, "Loose fat"),
)

FACTORS = (
    (0, "Choose your Activity Factor:"),
    (1.0, "1.0 - no exercise, desk job"),
    (1.2, "1.2 - little exercise, desk job"),
    (1.4, "1.4 - light exercise or sports 1-3 days/wk"),
    (1.6, "1.6 - moderate exercise or sports 3-5 days/wk"),
    (1.8, "1.8 - hard exercise or sports 6-7 days/wk"),
    (2.0, "2.0 - hard daily exercise or sports & physical labor job or 2 X day training, football camp, etc")
)

SEX = (
    (0, "Choose your gender:"),
    (1, "Woman"),
    (2, "Man"),
)

MEALS = (

    (1, "Breakfast"),
    (2, "Breakfast II"),
    (3, "Lunch"),
    (4, "Dinner"),
    (5, "Supper"),
)


class UserExtend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='static/foodfriend/img', null=True, blank=True)
    age = models.IntegerField(null=True, validators=[MaxValueValidator(150), MinValueValidator(1)])
    sex = models.IntegerField(choices=SEX, default=0)
    weight = models.IntegerField(null=True, validators=[MinValueValidator(1)])
    height = models.IntegerField(null=True, validators=[MinValueValidator(50)])
    factor = models.FloatField(choices=FACTORS, default=0)
    target = models.IntegerField(choices=TARGETS, default=0)
    creation_date = models.DateTimeField(default=timezone.now)


    @property
    def calories(self):
        if self.sex == 2:
            if self.age and self.weight and self.height and self.factor:
                if self.target == 1:
                    calories_count = int((66+13.7*self.weight+5*self.height-6.8*self.age)*self.factor+300)
                if self.target == 2:
                    calories_count = int((66+13.7*self.weight+5*self.height-6.8*self.age)*self.factor-300)
            else:
                calories_count = "No full data"

            return calories_count

        if self.sex == 1:
            if self.age and self.weight and self.height and self.factor:
                if self.target == 1:
                    calories_count = int((665+9.6*self.weight+1.85*self.height-4.7*self.age)*self.factor+300)
                if self.target == 2:
                    calories_count = int((665+9.6*self.weight+1.85*self.height-4.7*self.age)*self.factor-300)
            else:
                calories_count = "No full data"

            return calories_count

    @property
    def protein(self):
        if self.target == 1:
            result = int(self.calories*0.25/4)
        else:
            result = int(self.calories*0.3/4)
        return result

    @property
    def carb(self):
        if self.target == 1:
            result = int(self.calories*0.45/4)
        else:
            result = int(self.calories*0.5/4)
        return result

    @property
    def fat(self):
        if self.target == 1:
            result = int(self.calories*0.3/9)
        else:
            result = int(self.calories*0.2/9)
        return result

    @property
    def water(self):
        return int(self.calories)

    def __str__(self):
        return self.user.username

class Food(models.Model):
    name = models.CharField(max_length=124)
    kcal = models.FloatField()
    proteins = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    grams = models.FloatField(default=100, validators=[MinValueValidator(1)])


    def __str__(self):
        return '%s: kcal:%s / P:%s / C:%s / F:%s' % (self.name, self.kcal, self.proteins, self.carbs, self.fats)

class Days(models.Model):
    date = models.DateField(auto_now_add=True)
    date_user = models.ForeignKey(UserExtend)

    class Meta:
        unique_together = ('date', 'date_user')

    @property
    def day_calories(self):
        food_calories = Food.objects.filter(meal__day_id=self.id)
        cal = 0
        counter = []
        for index, p in enumerate(food_calories):
            container = Quantity.objects.filter(food_quantity__id=p.id, meal_quantity__day_id=self.id)
            if len(container) > 1 and food_calories[index].id not in counter:
                counter.append(food_calories[index].id)
                quant = 0
                for i in container:
                    quant += i.quantity
                cal += int(round(p.kcal * quant / p.grams, 0))
            if food_calories[index].id not in counter:
                quant = Quantity.objects.filter(food_quantity__id=p.id, meal_quantity__day_id=self.id)[0].quantity
                cal += int(round(p.kcal*quant/p.grams, 0))
        return cal

    @property
    def day_proteins(self):
        food_calories = Food.objects.filter(meal__day_id=self.id)
        protein = 0
        counter = []
        for index, p in enumerate(food_calories):
            container = Quantity.objects.filter(food_quantity__id=p.id, meal_quantity__day_id=self.id)
            if len(container) > 1 and food_calories[index].id not in counter:
                counter.append(food_calories[index].id)
                quant = 0
                for i in container:
                    quant += i.quantity
                protein += int(round(p.proteins * quant / p.grams, 0))
            if food_calories[index].id not in counter:
                quant = Quantity.objects.filter(food_quantity__id=p.id, meal_quantity__day_id=self.id)[0].quantity
                protein += int(round(p.proteins * quant / p.grams, 0))
        return protein

    @property
    def day_carbs(self):
        food_calories = Food.objects.filter(meal__day_id=self.id)
        carb = 0
        counter = []
        for index, p in enumerate(food_calories):
            container = Quantity.objects.filter(food_quantity__id=p.id, meal_quantity__day_id=self.id)
            if len(container) > 1 and food_calories[index].id not in counter:
                counter.append(food_calories[index].id)
                quant = 0
                for i in container:
                    quant += i.quantity
                carb += int(round(p.carbs * quant / p.grams, 0))
            if food_calories[index].id not in counter:
                quant = Quantity.objects.filter(food_quantity__id=p.id, meal_quantity__day_id=self.id)[0].quantity
                carb += int(round(p.carbs * quant / p.grams, 0))
        return carb

    @property
    def day_fats(self):
        food_calories = Food.objects.filter(meal__day_id=self.id)
        fat = 0
        counter = []
        for index, p in enumerate(food_calories):
            container = Quantity.objects.filter(food_quantity__id=p.id, meal_quantity__day_id=self.id)
            if len(container) > 1 and food_calories[index].id not in counter:
                counter.append(food_calories[index].id)
                quant = 0
                for i in container:
                    quant += i.quantity
                fat += int(round(p.fats * quant / p.grams, 0))
            if food_calories[index].id not in counter:
                quant = Quantity.objects.filter(food_quantity__id=p.id, meal_quantity__day_id=self.id)[0].quantity
                fat += int(round(p.fats * quant / p.grams, 0))
        return fat

    @property
    def day_water(self):
        water = 0
        container = Quantity.objects.filter(food_quantity__id=53, meal_quantity__day_id=self.id)
        for i in container:
            water += i.quantity
        return water

    def __str__(self):
        return "{}".format(self.date) #self.date_user


class Meal(models.Model):
    meal_name = models.IntegerField(choices=MEALS, default=1)
    day = models.ForeignKey(Days, null=True, blank=True)
    foods = models.ManyToManyField(Food, through='Quantity', blank=True)

    def __str__(self):
        return str(self.meal_name)

class Quantity(models.Model):
    meal_quantity = models.ForeignKey('Meal', on_delete=models.CASCADE, related_name="MealQuantity")
    food_quantity = models.ForeignKey('Food', on_delete=models.CASCADE, related_name="FoodQuantity")
    quantity = models.FloatField(default=100, blank=True, null=True, validators=[MinValueValidator(0)])

    @property
    def kcal_quant(self):
        calories = Food.objects.filter(FoodQuantity__id=self.id)[0].kcal
        grams = Food.objects.filter(FoodQuantity__id=self.id)[0].grams
        before_round = (calories*self.quantity) / grams
        result = math.ceil(before_round)
        return result

    @property
    def proteins_quant(self):
        proteins = Food.objects.filter(FoodQuantity__id=self.id)[0].proteins
        grams = Food.objects.filter(FoodQuantity__id=self.id)[0].grams
        before_round = (proteins * self.quantity) / grams
        result = math.ceil(before_round)
        return result

    @property
    def carbs_quant(self):
        carbs = Food.objects.filter(FoodQuantity__id=self.id)[0].carbs
        grams = Food.objects.filter(FoodQuantity__id=self.id)[0].grams
        before_round = (carbs * self.quantity) / grams
        result = math.ceil(before_round)
        return result

    @property
    def fats_quant(self):
        fats = Food.objects.filter(FoodQuantity__id=self.id)[0].fats
        grams = Food.objects.filter(FoodQuantity__id=self.id)[0].grams
        before_round = (fats * self.quantity) / grams
        result = math.ceil(before_round)
        return result


    def __str__(self):
        return 'meal: %s, quantity: %s, kcal: %s' % (self.meal_quantity, self.quantity, self.kcal_quant)














