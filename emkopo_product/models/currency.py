from django.db import models
from simple_history.models import HistoricalRecords

from emkopo_mixins.model import BaseUuidModel


class Currency(BaseUuidModel):
    name = models.CharField(
        verbose_name="Currency Name",
        max_length=45,
    )
    code = models.CharField(
        verbose_name="Currency Code",
        max_length=10,
    )
    status = models.IntegerField(
        verbose_name="Currency Status",
        default=1,
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Currency"
        verbose_name_plural = "Currency"
