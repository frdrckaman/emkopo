import sys

from django.apps import AppConfig as DjangoAppConfig
from django.core.management import color_style
from django.db.models.signals import post_migrate

from .role_names import groups_by_role_name, role_names
from .update_roles import update_roles

style = color_style()


def post_migrate_user_roles(sender=None, **kwargs):  # noqa
    """Update Role model with e-MKOPO defaults.

    To add custom roles, register this in your main
    app with additional role_names and groups_by_role_name.
    """
    update_roles(
        groups_by_role_name=groups_by_role_name, role_names=role_names, verbose=True
    )


class AppConfig(DjangoAppConfig):
    name = 'emkopo_auth'

    def ready(self):
        post_migrate.connect(post_migrate_user_roles, sender=self)
        sys.stdout.write(f"Loading {self.verbose_name} ...\n")
        sys.stdout.write(f" Done loading {self.verbose_name}.\n")
