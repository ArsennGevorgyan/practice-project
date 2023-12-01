from django.urls import path
from pizza.views import pizza, burger, about_us

urlpatterns = [
    path("", pizza, name="pizzas"),
    path("burgers/", burger, name="burgers"),
    path("about-us/", about_us, name="about_us")
]
