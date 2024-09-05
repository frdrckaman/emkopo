from django.db import models
from simple_history.models import HistoricalRecords

from emkopo_mixins.model import BaseUuidModel
from ..choices import THEME
from ..constants import LIGHT, DARK_THEME


class AppTheme(BaseUuidModel):
    theme_mode = models.CharField(
        verbose_name="Theme",
        max_length=8,
        choices=THEME,
        default=LIGHT,
    )
    theme_name = models.CharField(
        verbose_name="Theme Name",
        max_length=24,
        default=DARK_THEME,
    )
    theme_user = models.CharField(
        verbose_name="Username",
        max_length=12,
        blank=True,
        null=True,
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.theme_user

    class Meta(BaseUuidModel.Meta):
        verbose_name = "App Theme"
        verbose_name_plural = "App Theme"
