# Generated by Django 5.1 on 2024-09-25 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emkopo_loan", "0031_alter_historicalloanofferrequest_retirementdate_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalloanofferrequest",
            name="Sex",
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name="Sex"),
        ),
        migrations.AlterField(
            model_name="loanofferrequest",
            name="Sex",
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name="Sex"),
        ),
    ]