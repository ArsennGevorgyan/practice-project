from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Create and set permissions for business users"

    def handle(self, *args, **options):
        if not Group.objects.filter(name="business").exists():
            group = Group.objects.create(name="business")
            group.permissions.add(Permission.objects.get(codename="add_pizza"),
                                  Permission.objects.get(codename="change_pizza"),
                                  Permission.objects.get(codename="delete_pizza"),
                                  Permission.objects.get(codename="add_burger"),
                                  Permission.objects.get(codename="change_burger"),
                                  Permission.objects.get(codename="delete_burger"),
                                  Permission.objects.get(codename="add_restaurant"),
                                  Permission.objects.get(codename="change_restaurant"),
                                  Permission.objects.get(codename="delete_restaurant"),
                                  )
            self.stdout.write(self.style.SUCCESS(f"Group was set successfully!"))
