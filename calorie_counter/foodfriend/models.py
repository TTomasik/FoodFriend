from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    (0, "Choose meal type:"),
    (1, "Breakfast"),
    (2, "Breakfast II"),
    (3, "Lunch"),
    (4, "Dinner"),
    (5, "Supper"),
)


class UserExtend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='static/foodfriend/img', null=True, blank=True)
    age = models.IntegerField(null=True)
    sex = models.IntegerField(choices=SEX, default=0)
    weight = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    factor = models.FloatField(choices=FACTORS, default=0)
    target = models.IntegerField(choices=TARGETS, default=0)
    creation_date = models.DateTimeField(default=timezone.now)

    @property
    def calories(self):
        if self.sex == 2:
            if self.age and self.weight and self.height and self.factor:
                if self.target == 1:
                    calories_count = int((66.5+13.7*self.weight+5*self.height-6.8*self.age)*self.factor+300)
                if self.target == 2:
                    calories_count = int((66.5+13.7*self.weight+5*self.height-6.8*self.age)*self.factor-300)
            else:
                calories_count = "No full data"

            return calories_count

        if self.sex == 1:
            if self.age and self.weight and self.height and self.factor:
                if self.target == 1:
                    calories_count = int((66.5+9.6*self.weight+1.85*self.height-4.7*self.age)*self.factor+300)
                if self.target == 2:
                    calories_count = int((66.5+9.6*self.weight+1.85*self.height-4.7*self.age)*self.factor-300)
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

    def __str__(self):
        return self.user.username

class Food(models.Model):
    name = models.CharField(max_length=124)
    kcal = models.IntegerField()
    proteins = models.IntegerField()
    carbs = models.IntegerField()
    fats = models.IntegerField()
    grams = models.IntegerField(default=100)

    def __str__(self):
        return '%s: kcal:%s, P:%s, C:%s, F:%s' % (self.name, self.kcal, self.proteins, self.carbs, self.fats)

class Days(models.Model):
    date = models.DateField(auto_now_add=True)
    date_user = models.ForeignKey(UserExtend)

    class Meta:
        unique_together = ('date', 'date_user')

    @property
    def day_calories(self):
        food_calories = Food.objects.filter(meal__day=self)
        cal = 0
        for p in food_calories:
            cal += p.kcal
        return cal

    @property
    def day_proteins(self):
        food_proteins = Food.objects.filter(meal__day=self)
        protein = 0
        for p in food_proteins:
            protein += p.proteins
        return protein

    @property
    def day_carbs(self):
        food_carbs = Food.objects.filter(meal__day=self)
        carb = 0
        for p in food_carbs:
            carb += p.carbs
        return carb

    @property
    def day_fats(self):
        food_fats = Food.objects.filter(meal__day=self)
        fat = 0
        for p in food_fats:
            fat += p.fats
        return fat

    def __str__(self):
        return "{} - {}".format(self.date, self.date_user)


class Meal(models.Model):
    meal_name = models.IntegerField(choices=MEALS, default=0)
    day = models.ForeignKey(Days, null=True, blank=True)
    foods = models.ManyToManyField(Food, blank=True)

    def __str__(self):
        return '%s: %s' % (self.meal_name, self.foods)


# class Movie(models.Model):
#     title = models.CharField(max_length=128)
#     director = models.ForeignKey('Person', related_name='movie_director')
#     screenplay = models.ForeignKey('Person', related_name='movie_screenplay')
#     starring = models.ManyToManyField('Person', through='Role', blank=True)
#     year = models.SmallIntegerField()
#     ranking = models.IntegerField(choices=RANKS, default=0)
#
#     def __str__(self):
#         return self.title
#
#
# class Role(models.Model):
#     person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name="Movie")
#     movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name="Movie")
#     role = models.CharField(max_length=128, primary_key=True)

class Quantity(models.Model):
    pass