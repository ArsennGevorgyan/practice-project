from django.urls import path
from pizza.views import pizza, burger, about_us,\
    all_restaurant, restaurant_detail, pizza_detail, burger_detail, \
    advanced_search

urlpatterns = [
    path("", pizza, name="pizzas"),
    path("pizza/detail/<int:pk>/", pizza_detail, name="pizza_details"),
    path("burger/detail/<int:pk>/", burger_detail, name="burger_detail"),
    path("burgers/", burger, name="burgers"),
    path("about-us/", about_us, name="about_us"),
    path("restaurants/", all_restaurant, name="restaurants"),
    path("restaurant/<int:pk>/", restaurant_detail, name="res_detail"),
    path("search/", advanced_search, name="search"),
]
