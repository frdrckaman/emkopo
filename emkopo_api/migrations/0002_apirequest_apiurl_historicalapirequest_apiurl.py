# Generated by Django 5.1 on 2024-09-11 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emkopo_api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="apirequest",
            name="ApiUrl",
            field=models.CharField(default="", max_length=255, verbose_name="ApiUrl"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalapirequest",
            name="ApiUrl",
            field=models.CharField(default="", max_length=255, verbose_name="ApiUrl"),
            preserve_default=False,
        ),
    ]