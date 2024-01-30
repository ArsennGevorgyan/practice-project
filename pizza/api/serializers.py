from rest_framework import serializers

from pizza.models import Pizza, Restaurant


class PizzaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pizza
        exclude = ("image", "restaurant")


class RestaurantSerializer(serializers.ModelSerializer):
    pizza = PizzaSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        exclude = ("owner", "image")
