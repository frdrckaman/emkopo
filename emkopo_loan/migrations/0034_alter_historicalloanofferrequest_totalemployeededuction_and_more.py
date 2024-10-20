# Generated by Django 5.1 on 2024-09-25 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emkopo_loan", "0033_alter_historicalloanofferrequest_bankaccountnumber_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalloanofferrequest",
            name="TotalEmployeeDeduction",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=40,
                null=True,
                verbose_name="Total Employee Deduction",
            ),
        ),
        migrations.AlterField(
            model_name="loanofferrequest",
            name="TotalEmployeeDeduction",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=40,
                null=True,
                verbose_name="Total Employee Deduction",
            ),
        ),
    ]
