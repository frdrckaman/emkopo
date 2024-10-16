from django.db import models
from simple_history.models import HistoricalRecords

from emkopo_mixins.model import BaseUuidModel
from .district import District


class Branch(BaseUuidModel):
    District = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_query_name='district',
        verbose_name="District",
    )
    BranchCode = models.CharField(
        verbose_name="Branch Code",
        max_length=120,
    )
    BranchName = models.CharField(
        verbose_name="Branch Name",
        max_length=255,
    )
    active = models.BooleanField(
        verbose_name="Status",
        default=True,
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.BranchCode

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Branch"
        verbose_name_plural = "Branchs"
