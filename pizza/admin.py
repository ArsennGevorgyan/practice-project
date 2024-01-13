from django.contrib import admin
from django.utils.html import format_html

from pizza.models import Pizza, Burger, Restaurant

from django.templatetags.static import static


class PizzaAdmin(admin.ModelAdmin):
    list_display = ("pizza_name", "rate", "prepare_time")
    search_fields = ("pizza_name",)
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at", "thumbnail")
    fieldsets = (
        (
            "GENERAL",
            {"fields": ("pizza_name", "rate", "prepare_time", "calories", "price")},
        ),
        (
            "INFO",
            {
                "fields": (
                    "restaurant",
                    "description",
                    ("image", "thumbnail"),
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @staticmethod
    def thumbnail(obj):
        return format_html(
            "<img src='{}' class='thumbnail'>",
            obj.image.url if obj.image else static("img/no_image.jpeg"),
        )


class BurgerAdmin(admin.ModelAdmin):
    list_display = ("burger_name", "rate", "prepare_time")
    search_fields = ("burger_name",)
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at", "thumbnail")
    fieldsets = (
        (
            "GENERAL",
            {"fields": ("burger_name", "rate", "prepare_time", "calories", "price")},
        ),
        (
            "INFO",
            {
                "fields": (
                    "restaurant",
                    "description",
                    ("image", "thumbnail"),
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @staticmethod
    def thumbnail(obj):
        return format_html(
            "<img src='{}' class='thumbnail'>",
            obj.image.url if obj.image else static("img/no_image.jpeg"),
        )


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "creation_date")
    search_fields = ("name",)


admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Burger, BurgerAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
