from django.db import models
from simple_history.models import HistoricalRecords

from emkopo_mixins.model import BaseUuidModel


class Fsp(BaseUuidModel):
    name = models.CharField(
        verbose_name="FSP Name",
        max_length=100,
    )
    sysName = models.CharField(
        verbose_name="System Name",
        max_length=45,
        default='FSPSystem'
    )
    code = models.CharField(
        verbose_name="FSP Code",
        max_length=10,
    )
    FSPBankAccount = models.CharField(
        verbose_name="FSP Bank Account",
        max_length=45,
        blank=True,
        null=True,
    )
    FSPBankAccountName = models.CharField(
        verbose_name="FSP Bank Account Name",
        max_length=45,
        blank=True,
        null=True,
    )
    SWIFTCode = models.CharField(
        verbose_name="SWIFT Code",
        max_length=45,
        blank=True,
        null=True,
    )
    MNOChannels = models.CharField(
        verbose_name="MNO Channels",
        max_length=45,
        blank=True,
        null=True,
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
        verbose_name_plural = "Financial Service Providers"
