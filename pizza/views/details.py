from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, modelformset_factory
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib import messages

from helpers.decorators import own_restaurant_product
from helpers.utils import get_similar_products
from pizza.forms import PizzaForm, BurgerForm, RestaurantForm, \
    restaurant_pizza_inline, restaurant_burger_inline
from pizza.models import Pizza, Restaurant, Burger


def pizza_detail(request, pk: int):
    pizza_inst = get_object_or_404(Pizza, pk=pk)
    editable = False
    if pizza_inst.restaurant.owner == request.user:
        editable = True
    similar_products = get_similar_products(Pizza, pizza_inst)
    return render(
        request,
        "details/pizza_detail.html",
        {"pizza": pizza_inst,
         "similar_products": similar_products,
         "editable": editable},
    )


def burger_detail(request, pk: int):
    burger_inst = get_object_or_404(Burger, pk=pk)
    editable = False
    if burger_inst.restaurant.owner == request.user:
        editable = True
    similar_products = get_similar_products(Burger, burger_inst)
    return render(
        request,
        "details/burger_detail.html",
        {"burger": burger_inst,
         "similar_products": similar_products,
         "editable": editable},
    )


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    editable = False
    if restaurant.owner == request.user:
        editable = True
    items = restaurant.pizza.all()
    if burgers := request.GET.get("burgers"):
        if burgers == "True":
            items = restaurant.burger.all()

    return render(
        request,
        "pizza/restaurant_detail.html",
        {"restaurant": restaurant,
         "items": items, "editable": editable}
    )


def add_pizza(request):
    if not request.user.has_perm("pizza.add_pizza"):
        messages.warning(request, "You don't have permissions for this action")
        return redirect("pizzas")
    form = PizzaForm(owner=request.user)
    if request.method == "POST":
        form = PizzaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Pizza added successfully!")
            return redirect("pizzas")
    return render(request, "details/add_pizza.html", {"form": form})


def add_burger(request):
    if not request.user.has_perm("pizza.add_burger"):
        messages.warning(request, "You don't have permissions for this action")
        return redirect("pizzas")
    form = BurgerForm(owner=request.user)

    if request.method == "POST":
        form = BurgerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Burger added successfully!")
            return redirect("burgers")
    return render(request, "details/add_burger.html", {"form": form})


@own_restaurant_product(product="pizza")
def edit_pizza(request, pk: int):
    if not request.user.has_perm("pizza.change_pizza"):
        messages.warning(request, "You don't have permissions for this action")
        return redirect("pizzas")
    pizza = get_object_or_404(Pizza, pk=pk)
    form = PizzaForm(instance=pizza)
    if request.method == "POST":
        form = PizzaForm(request.POST, request.FILES, instance=pizza)
        if form.is_valid():
            pizza_instance = form.save()
            messages.success(request, f"{pizza_instance.pizza_name} Updated successfully!")
            return redirect(pizza_instance)
    return render(request, "details/edit_pizza.html", {"form": form})


@own_restaurant_product(product="burger")
def edit_burger(request, pk: int):
    if not request.user.has_perm("pizza.change_burger"):
        messages.warning(request, "You don't have permissions for this action")
        return redirect("pizzas")
    burger = get_object_or_404(Burger, pk=pk)
    form = BurgerForm(instance=burger)
    if request.method == "POST":
        form = BurgerForm(request.POST, request.FILES, instance=burger)
        if form.is_valid():
            burger_instance = form.save()
            messages.success(request, f"{burger_instance.burger_name} Updated successfully!")
            return redirect(burger_instance)
    return render(request, "details/edit_burger.html", {"form": form})


@own_restaurant_product(product="pizza")
def delete_pizza(request, pk: int):
    if not request.user.has_perm("pizza.delete_pizza"):
        messages.warning(request, "You don't have permissions for this action")
        return redirect("pizzas")
    pizza = get_object_or_404(Pizza, pk=pk)
    if request.method == "POST":
        pizza.delete()
        messages.info(request, "pizza deleted Successfully")
        return redirect("pizzas")
    return render(request, "details/delete_pizza.html", {"pizza": pizza})


@own_restaurant_product(product="burger")
def delete_burger(request, pk: int):
    if not request.user.has_perm("pizza.delete_burger"):
        messages.warning(request, "You don't have permissions for this action")
        return redirect("pizzas")
    burger = get_object_or_404(Burger, pk=pk)
    if request.method == "POST":
        burger.delete()
        messages.info(request, "Burger deleted successfully!")
        return redirect("burgers")
    return render(request, "details/delete_burger.html", {"burger": burger})


@login_required()
def add_restaurant(request):
    if not request.user.has_perm("pizza.add_restaurant"):
        messages.warning(request, "You don't have permissions for this action")
        return redirect("pizzas")
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
        restaurant = restaurant_form.save(commit=False)
        restaurant.owner = request.user
        restaurant.save()
        for inst in related_data:
            inst.restaurant = restaurant
            inst.save()
        messages.success(request, f"Your {restaurant.name} Created Successfully")
        return redirect("pizzas")

    context = {"form": restaurant_form,
               "restaurant_burger_formset": restaurant_burger_formset,
               "restaurant_pizza_formset": restaurant_pizza_formset}
    return render(request, "details/add_restaurant.html", context)
