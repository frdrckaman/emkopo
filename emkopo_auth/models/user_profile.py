from django.contrib.auth.models import Group, User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _

from .role import Role
from ..constants import CUSTOM_ROLE, STAFF_ROLE


class UserProfile(models.Model):
    email_notifications = models.BooleanField(
        verbose_name="Email Notifications",
        default=False
    )

    sms_notifications = models.BooleanField(
        verbose_name='SMS Notification',
        default=True,
    )

    user = models.OneToOneField(User, on_delete=CASCADE)

    job_title = models.CharField(max_length=100, null=True, blank=True)

    alternate_email = models.EmailField(
        _("Alternate email address"), blank=True, null=True
    )

    mobile = models.CharField(
        max_length=25,
        validators=[RegexValidator(regex="^\\+\\d+")],
        null=True,
        blank=True,
        help_text="e.g. +0123456789",
    )

    roles = models.ManyToManyField(Role, blank=True)

    def __str__(self):
        return self.user.username

    def add_groups_for_roles(self, pk_set):
        """Add groups to this user for the selected roles.

        Called by m2m signal.
        """
        if CUSTOM_ROLE not in [obj.name for obj in self.roles.all()]:
            group_names = [group.name for group in self.user.groups.all()]
            add_group_names = []
            for role in self.roles.all():
                for group in role.groups.all():
                    if group.name not in group_names:
                        add_group_names.append(group.name)
            add_group_names = list(set(add_group_names))
            for name in add_group_names:
                self.user.groups.add(Group.objects.get(name=name))
                self.user.save()

    def remove_groups_for_roles(self, pk_set):
        """Remove groups from this user for the removed roles.

        Called by m2m signal.
        """
        if CUSTOM_ROLE in [obj.name for obj in Role.objects.filter(pk__in=pk_set)]:
            self.user.groups.clear()
            self.user.userprofile.roles.clear()
            self.user.userprofile.roles.add(Role.objects.get(name=STAFF_ROLE))
        else:
            remove_group_names = []
            current_group_names = []
            for role in self.roles.all():
                current_group_names.extend([group.name for group in role.groups.all()])
            for role in Role.objects.filter(pk__in=pk_set):
                remove_group_names.extend(
                    [
                        group.name
                        for group in role.groups.all()
                        if group.name not in current_group_names
                    ]
                )
            for name in remove_group_names:
                self.user.groups.remove(Group.objects.get(name=name))