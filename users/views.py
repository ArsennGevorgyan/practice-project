from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib.auth.views import LoginView, LogoutView

from helpers.mixins import OwnProFileMixin
from users.forms import UserRegistrationForm, ProfileForm


class UserCreationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "user/registration.html"
    success_url = reverse_lazy("pizzas")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.profile.phone_number = form.cleaned_data["phone_number"]
        self.object.profile.country = form.cleaned_data["country"]
        self.object.profile.image = form.cleaned_data["image"]
        self.object.profile.user_type = form.cleaned_data["user_type"]
        self.object.profile.save()
        messages.success(self.request, "User Created Successfully")
        return response


class UserLoginView(LoginView):
    template_name = "user/login.html"


class UserLogoutView(LogoutView):
    pass


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "user/profile.html"


class UserUpdateView(OwnProFileMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "user/edit_profile.html"

    def get_initial(self):
        return {"phone_number": self.object.profile.phone_number,
                "country": self.object.profile.country,
                "image": self.object.profile.image}

    def get_success_url(self):
        messages.success(self.request, "User updated successfully!")
        return reverse("profile", kwargs={"pk": self.object.pk})

