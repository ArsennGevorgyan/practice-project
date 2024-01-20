import copy

from django.shortcuts import reverse
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as AdminGroup
from django.contrib.auth.models import Group
from django.utils.html import format_html

from users.models import Profile


class GroupAdmin(AdminGroup):
    readonly_fields = ("send_email_to_group",)

    @staticmethod
    def send_email_to_group(obj):
        return format_html(
            "<button type=submit style='background-color:#4aed09;'><a href='{}'>Submit</a></button>",
            reverse("business_email", kwargs={
                "group_id": obj.pk
            }),
        )


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(Profile)
