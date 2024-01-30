from django.urls import path

from pizza.api.views import PizzaListCreateAPIView, ListRestaurantAPIView

urlpatterns = [
    path("<int:restaurant_pk>/", PizzaListCreateAPIView.as_view()),
    path("restaurants/", ListRestaurantAPIView.as_view()),
]