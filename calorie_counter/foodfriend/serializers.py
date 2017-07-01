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
    class Meta:
        model = Days
        fields = '__all__'