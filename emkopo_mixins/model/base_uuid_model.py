from django.db import models
from django_audit_fields.models import AuditUuidModelMixin


class BaseUuidModel(AuditUuidModelMixin, models.Model):
    objects = models.Manager()

    class Meta(AuditUuidModelMixin.Meta):
        abstract = True
        default_permissions = ("add", "change", "delete", "view", "export", "import")