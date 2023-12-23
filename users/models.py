from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from helpers.choices import UserTypeChoice
from helpers.media_upload import upload_user_images
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_user_images, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=UserTypeChoice.choices)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def profile_post_save(instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
