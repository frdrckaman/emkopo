# Generated by Django 5.1 on 2024-09-15 14:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emkopo_loan", "0012_historicalloanofferrequest_timestamp_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalloanchargerequest",
            name="Timestamp",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Timestamp"
            ),
        ),
        migrations.AddField(
            model_name="historicalloanchargeresponse",
            name="Timestamp",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Timestamp"
            ),
        ),
        migrations.AddField(
            model_name="historicalloanofferresponse",
            name="Timestamp",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Timestamp"
            ),
        ),
        migrations.AddField(
            model_name="loanchargerequest",
            name="Timestamp",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Timestamp"
            ),
        ),
        migrations.AddField(
            model_name="loanchargeresponse",
            name="Timestamp",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Timestamp"
            ),
        ),
        migrations.AddField(
            model_name="loanofferresponse",
            name="Timestamp",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Timestamp"
            ),
        ),
    ]
