from django.urls import path
from pizza.views import pizza, burger, about_us, all_restaurant, restaurant_detail

urlpatterns = [
    path("", pizza, name="pizzas"),
    path("burgers/", burger, name="burgers"),
    path("about-us/", about_us, name="about_us"),
    path("restaurants/", all_restaurant, name="restaurants"),
    path("restaurant/<int:pk>/", restaurant_detail, name="res_detail")
]
