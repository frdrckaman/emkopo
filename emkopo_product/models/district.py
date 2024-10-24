from django.db import models
from simple_history.models import HistoricalRecords

from emkopo_mixins.model import BaseUuidModel


class District(BaseUuidModel):
    DistrictNane = models.CharField(
        verbose_name="District Name",
        max_length=120,
    )
    DistrictCode = models.CharField(
        verbose_name="District Code",
        max_length=45,
    )
    active = models.BooleanField(
        verbose_name="Status",
        default=True
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.DistrictCode

    class Meta(BaseUuidModel.Meta):
        verbose_name = "District"
        verbose_name_plural = "Districts"
