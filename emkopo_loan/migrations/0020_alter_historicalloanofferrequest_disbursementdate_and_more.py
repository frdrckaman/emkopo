# Generated by Django 5.1 on 2024-09-16 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emkopo_loan", "0019_historicalloanofferrequest_disbursementdate_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalloanofferrequest",
            name="DisbursementDate",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Disbursement date"
            ),
        ),
        migrations.AlterField(
            model_name="loanofferrequest",
            name="DisbursementDate",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Disbursement date"
            ),
        ),
    ]