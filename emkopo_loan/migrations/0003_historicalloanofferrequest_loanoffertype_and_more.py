# Generated by Django 5.1 on 2024-09-13 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emkopo_loan", "0002_alter_historicalloanchargerequest_requesttype_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalloanofferrequest",
            name="LoanOfferType",
            field=models.CharField(
                choices=[
                    ("new_loan", "NEW LOAN"),
                    ("top_up_loan", "TOP UP LOAN"),
                    ("take_over_loan", "TAKE OVER LOAN"),
                ],
                default="new_loan",
                max_length=45,
                verbose_name="Loan Offer Type",
            ),
        ),
        migrations.AddField(
            model_name="loanofferrequest",
            name="LoanOfferType",
            field=models.CharField(
                choices=[
                    ("new_loan", "NEW LOAN"),
                    ("top_up_loan", "TOP UP LOAN"),
                    ("take_over_loan", "TAKE OVER LOAN"),
                ],
                default="new_loan",
                max_length=45,
                verbose_name="Loan Offer Type",
            ),
        ),
    ]