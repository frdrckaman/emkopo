from django.db import models
from simple_history.models import HistoricalRecords

from emkopo_mixins.model import BaseUuidModel


class Fsp(BaseUuidModel):
    name = models.CharField(
        verbose_name="FSP Name",
        max_length=84,
    )
    code = models.CharField(
        verbose_name="FSP Code",
        max_length=45,
    )
    status = models.IntegerField(
        verbose_name="FSP Status",
        default=1,
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Financial Service Provider"
        verbose_name_plural = "Financial Service ProviderS"
