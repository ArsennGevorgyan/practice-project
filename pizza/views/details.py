from django.forms import formset_factory, modelformset_factory
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib import messages

from helpers.utils import get_similar_products
from pizza.forms import PizzaForm, BurgerForm, RestaurantForm, \
    restaurant_pizza_inline, restaurant_burger_inline
from pizza.models import Pizza, Restaurant, Burger


def pizza_detail(request, pk: int):
    pizza_inst = get_object_or_404(Pizza, pk=pk)
    similar_products = get_similar_products(Pizza, pizza_inst)
    return render(
        request,
        "details/pizza_detail.html",
        {"pizza": pizza_inst, "similar_products": similar_products},
    )


def burger_detail(request, pk: int):
    burger_inst = get_object_or_404(Burger, pk=pk)
    similar_products = get_similar_products(Burger, burger_inst)
    return render(
        request,
        "details/burger_detail.html",
        {"burger": burger_inst, "similar_products": similar_products},
    )


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


def add_pizza(request):
    form = PizzaForm()
    if request.method == "POST":
        form = PizzaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Pizza added successfully!")
            return redirect("pizzas")
    return render(request, "details/add_pizza.html", {"form": form})


def add_burger(request):
    form = BurgerForm()
    if request.method == "POST":
        form = BurgerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Burger added successfully!")
            return redirect("burgers")
    return render(request, "details/add_burger.html", {"form": form})


def edit_pizza(request, pk: int):
    pizza = get_object_or_404(Pizza, pk=pk)
    form = PizzaForm(instance=pizza)
    if request.method == "POST":
        form = PizzaForm(request.POST, request.FILES, instance=pizza)
        if form.is_valid():
            pizza_instance = form.save()
            messages.success(request, f"{pizza_instance.pizza_name} Updated successfully!")
            return redirect(pizza_instance)
    return render(request, "details/edit_pizza.html", {"form": form})


def edit_burger(request, pk: int):
    burger = get_object_or_404(Burger, pk=pk)
    form = BurgerForm(instance=burger)
    if request.method == "POST":
        form = BurgerForm(request.POST, request.FILES, instance=burger)
        if form.is_valid():
            burger_instance = form.save()
            messages.success(request, f"{burger_instance.burger_name} Updated successfully!")
            return redirect(burger_instance)
    return render(request, "details/edit_burger.html", {"form": form})


def delete_pizza(request, pk: int):
    pizza = get_object_or_404(Pizza, pk=pk)
    if request.method == "POST":
        pizza.delete()
        messages.info(request, "pizza deleted Successfully")
        return redirect("pizzas")
    return render(request, "details/delete_pizza.html", {"pizza": pizza})


def delete_burger(request, pk: int):
    burger = get_object_or_404(Burger, pk=pk)
    if request.method == "POST":
        burger.delete()
        messages.info(request, "Burger deleted successfully!")
        return redirect("burgers")
    return render(request, "details/delete_burger.html", {"burger": burger})


def add_restaurant(request):
    related_data = []
    restaurant_form = RestaurantForm(request.POST or None, request.FILES or None)
    restaurant_pizza_formset = restaurant_pizza_inline(request.POST or None, request.FILES or None)
    restaurant_burger_formset = restaurant_burger_inline(request.POST or None, request.FILES or None)
    if restaurant_form.is_valid():
        for form in list(restaurant_pizza_formset) + list(restaurant_burger_formset):
            if form.is_valid():
                if form.cleaned_data:
                    instance = form.save(commit=False)
                    related_data.append(instance)
            else:
                for field, err in form.errors.items():
                    error_text = ','.join([e for e in err])
                    messages.error(request, f"{field}! {error_text}")
                    return redirect("add_restaurant")
        restaurant = restaurant_form.save()
        for inst in related_data:
            inst.restaurant = restaurant
            inst.save()
        messages.success(request, f"Your {restaurant.name} Created Successfully")
        return redirect("pizzas")

    context = {"form": restaurant_form,
               "restaurant_burger_formset": restaurant_burger_formset,
               "restaurant_pizza_formset": restaurant_pizza_formset}
    return render(request, "details/add_restaurant.html", context)
