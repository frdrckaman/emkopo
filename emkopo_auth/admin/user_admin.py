from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from emkopo_auth.admin.user_profile_admin import UserProfileInline
from emkopo_dashboard.utils import select_idap_template

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    form = UserChangeForm

    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "userprofile__roles__name",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "userprofile__roles",
        "groups",
    )

    @staticmethod
    def role(obj=None):
        roles = []
        role_group_names = []
        for role in obj.userprofile.roles.all():
            roles.append(role)
            role_group_names.extend(
                [grp.name for grp in role.groups.all().order_by("name")]
            )
        extra_groups = [
            obj for obj in obj.groups.all() if obj.name not in role_group_names
        ]
        context = dict(
            role_names=[role.display_name for role in roles],
            extra_group_names=[grp.name.replace("_", " ") for grp in extra_groups],
        )
        template_obj = select_idap_template("user_role_description.html", "emkopo_auth")
        return render_to_string(template_obj.template.name, context)

    @staticmethod
    def groups_in_role(obj=None):
        roles = []
        role_group_names = []
        for role in obj.userprofile.roles.all():
            roles.append(role)
            role_group_names.extend(
                [grp.name for grp in role.groups.all().order_by("name")]
            )
        extra_groups = [
            obj for obj in obj.groups.all() if obj.name not in role_group_names
        ]
        context = dict(
            role_names=[role.display_name for role in roles],
            extra_group_names=[grp.name.replace("_", " ") for grp in extra_groups],
        )
        template_obj = select_idap_template("user_role_description.html", "emkopo_auth")
        return render_to_string(template_obj.template.name, context)