# Generated by Django 5.1 on 2024-09-15 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emkopo_loan", "0014_historicaluserresponse_applicationnumber_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicaluserresponse",
            name="FspResponse",
            field=models.CharField(
                choices=[
                    ("2", "ACCEPT"),
                    ("9", "REJECT"),
                    ("4", "DISBURSED"),
                    ("5", "NOT DISBURSED"),
                ],
                default="0",
                max_length=10,
                verbose_name="Offer Response",
            ),
        ),
        migrations.AlterField(
            model_name="userresponse",
            name="FspResponse",
            field=models.CharField(
                choices=[
                    ("2", "ACCEPT"),
                    ("9", "REJECT"),
                    ("4", "DISBURSED"),
                    ("5", "NOT DISBURSED"),
                ],
                default="0",
                max_length=10,
                verbose_name="Offer Response",
            ),
        ),
    ]