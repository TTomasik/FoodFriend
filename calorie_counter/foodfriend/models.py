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







    def __str__(self):
        return '%s is %s' % (self.user.username, self.avatar)

