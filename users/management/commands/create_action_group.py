from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Create and set permissions for busines users"

    def handle(self, *args, **options):
        if not Group.objects.filter(name="product_action").exists():
            group = Group.objects.create(name="product_action")
            group.permissions.add(Permission.objects.get(codename="add_pizza"),
                                  Permission.objects.get(codename="change_pizza"),
                                  Permission.objects.get(codename="delete_pizza"),
                                  Permission.objects.get(codename="add_burger"),
                                  Permission.objects.get(codename="change_burger"),
                                  Permission.objects.get(codename="delete_burger"),
                                  )
            self.stdout.write(self.style.SUCCESS(f"Group was set successfully!"))


