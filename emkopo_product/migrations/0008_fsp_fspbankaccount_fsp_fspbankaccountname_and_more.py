# Generated by Django 5.1 on 2024-09-17 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emkopo_product", "0007_fsp_sysname_historicalfsp_sysname"),
    ]

    operations = [
        migrations.AddField(
            model_name="fsp",
            name="FSPBankAccount",
            field=models.CharField(
                blank=True, max_length=45, null=True, verbose_name="FSP Bank Account"
            ),
        ),
        migrations.AddField(
            model_name="fsp",
            name="FSPBankAccountName",
            field=models.CharField(
                blank=True, max_length=45, null=True, verbose_name="FSP Bank Account Name"
            ),
        ),
        migrations.AddField(
            model_name="fsp",
            name="MNOChannels",
            field=models.CharField(
                blank=True, max_length=45, null=True, verbose_name="MNO Channels"
            ),
        ),
        migrations.AddField(
            model_name="fsp",
            name="SWIFTCode",
            field=models.CharField(
                blank=True, max_length=45, null=True, verbose_name="SWIFT Code"
            ),
        ),
        migrations.AddField(
            model_name="historicalfsp",
            name="FSPBankAccount",
            field=models.CharField(
                blank=True, max_length=45, null=True, verbose_name="FSP Bank Account"
            ),
        ),
        migrations.AddField(
            model_name="historicalfsp",
            name="FSPBankAccountName",
            field=models.CharField(
                blank=True, max_length=45, null=True, verbose_name="FSP Bank Account Name"
            ),
        ),
        migrations.AddField(
            model_name="historicalfsp",
            name="MNOChannels",
            field=models.CharField(
                blank=True, max_length=45, null=True, verbose_name="MNO Channels"
            ),
        ),
        migrations.AddField(
            model_name="historicalfsp",
            name="SWIFTCode",
            field=models.CharField(
                blank=True, max_length=45, null=True, verbose_name="SWIFT Code"
            ),
        ),
    ]