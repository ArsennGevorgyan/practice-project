from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, ListView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import Group
from helpers.mixins import OwnProFileMixin
from users.forms import UserRegistrationForm, ProfileForm, EmailForm
from django.conf import settings


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
        if self.object.profile.user_type == "business":
            restaurant_group = Group.objects.get(name="product_action")
            restaurant_group.user_set.add(self.object)
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


class BusinessEmailView(FormView):
    template_name = "group/business_email.html"
    form_class = EmailForm

    def form_valid(self, form):
        response = super().form_valid(form)
        subject = form.cleaned_data['subject']
        body = form.cleaned_data['body']
        users = User.objects.filter(groups__pk=self.kwargs["group_id"])
        send_mass_mail(datatuple=[(subject, body,
                                   settings.EMAIL_HOST_USER,
                                   [user.email])for user in users])
        return response

    def get_success_url(self):
        messages.success(self.request, "Messages send successfully")
        return reverse("admin:auth_group_changelist")
