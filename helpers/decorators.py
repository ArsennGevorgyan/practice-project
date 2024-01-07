from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def profile_decorator(func: callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.user.pk != kwargs.get("pk"):
            messages.error(request, "Invalid attempt!")
            return redirect("pizzas")
        return func(*args, **kwargs)
    return wrapper


def own_restaurant_product(product: str):

    def wrapper_func(func: callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = args[0]
            if kwargs.get("pk") not in request.user \
                    .restaurant_set.only(f"{product}__id") \
                    .values_list(f"{product}__id", flat=True):
                messages.error(request, "You don't have permission to do this action!")
                return redirect("pizzas")
            return func(*args, **kwargs)
        return wrapper
    return wrapper_func
