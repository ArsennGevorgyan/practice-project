from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from pizza.forms import SearchForm
from pizza.models import Pizza, Burger, Restaurant


def pizza(request):
    pizzas = Pizza.objects.all()
    paginator = Paginator(pizzas, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "pizza/all_pizza.html", {"pizzas": page_obj})


def pizza_detail(request, pk: int):
    pizza_inst = get_object_or_404(Pizza, pk=pk)
    similar_products = Pizza.objects.filter(
        (Q(price__lte=pizza_inst.price + 5) & Q(price__gte=pizza_inst.price - 5))
        | (
            Q(calories__lte=pizza_inst.calories + 5)
            & Q(calories__gte=pizza_inst.calories - 5)
        ),
        ~Q(id=pizza_inst.id),
    )
    return render(
        request,
        "details/pizza_detail.html",
        {"pizza": pizza_inst, "similar_products": similar_products},
    )


def burger(request):
    burgers = Burger.objects.all()
    paginator = Paginator(burgers, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "pizza/burgers.html", {"burgers": page_obj})


def burger_detail(request, pk: int):
    burger_inst = get_object_or_404(Burger, pk=pk)
    similar_products = Burger.objects.filter(
        (Q(price__lte=burger_inst.price + 5) & Q(price__gte=burger_inst.price - 5))
        | (
            Q(calories__lte=burger_inst.calories + 5)
            & Q(calories__gte=burger_inst.calories - 5)
        ),
        ~Q(id=burger_inst.id),
    )
    return render(
        request,
        "details/burger_detail.html",
        {"burger": burger_inst, "similar_products": similar_products},
    )


def all_restaurant(request):
    restaurants = Restaurant.objects.all().order_by("pk")
    paginator = Paginator(restaurants, 6)
    page_number = request.GET.get("page")
    restaurants = paginator.get_page(page_number)
    return render(request, "pizza/restaurants.html", {"restaurants": restaurants})


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    items = restaurant.pizza.all()
    if burgers := request.GET.get("burgers"):
        if burgers == "True":
            items = restaurant.burger.all()

    return render(
        request,
        "pizza/restaurant_detail.html",
        {"restaurant": restaurant, "items": items},
    )


def advanced_search(request):
    form = SearchForm()
    result_product = []
    if name := request.GET.get("name"):
        form = SearchForm(request.GET)
        if request.GET.get("product_type") == "burger":
            product_table = Burger
            name_search = Q(burger_name__icontains=name)
        else:
            product_table = Pizza
            name_search = Q(pizza_name__icontains=name)
        if form.is_valid():
            result_product = product_table.objects.filter(
                name_search | (Q(
                    rate__lte=form.cleaned_data.get("rate_until") or 0
                ) & Q(rate__gte=form.cleaned_data.get("rate_from" or 0)))
                | Q(calories__lte=form.cleaned_data.get("calories_until") or 0)
            )
    return render(request, "pizza/search.html", {"form": form,
                                                 "result_product": result_product})


def about_us(request):
    return render(request, "pizza/about_us.html")
