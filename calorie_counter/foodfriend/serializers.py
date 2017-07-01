from rest_framework import serializers
from foodfriend.models import Food, UserExtend, Days


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtend
        fields = '__all__'

class DaysSerializer(serializers.ModelSerializer):
    day_calories = serializers.ReadOnlyField()
    day_proteins = serializers.ReadOnlyField()
    day_carbs = serializers.ReadOnlyField()
    day_fats = serializers.ReadOnlyField()
    day_water = serializers.ReadOnlyField()

    class Meta:
        model = Days
        fields = '__all__'