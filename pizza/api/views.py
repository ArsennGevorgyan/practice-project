from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, ListAPIView

from helpers.mixins import OwnProFileMixin
from pizza.api.pagination import CustomPagination
from pizza.api.permissions import IsBusinessUser
from pizza.api.serializers import PizzaSerializer, RestaurantSerializer
from pizza.models import Pizza, Restaurant


class PizzaListCreateAPIView(ListCreateAPIView):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    permission_classes = [IsBusinessUser]

    def get_queryset(self):
        restaurant_pk = self.kwargs.get("restaurant_pk")
        return Pizza.objects.filter(restaurant=restaurant_pk)

    def perform_create(self, serializer):
        restaurant_pk = self.kwargs.get("restaurant_pk")
        restaurant_instance = Restaurant.objects.get(pk=restaurant_pk)
        serializer.save(restaurant=restaurant_instance)


class ListRestaurantAPIView(ListCreateAPIView):
    queryset = Restaurant.objects.all().order_by("-pk")
    serializer_class = RestaurantSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

