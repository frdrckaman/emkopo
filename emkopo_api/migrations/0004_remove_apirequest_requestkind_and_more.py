# Generated by Django 4.2.15 on 2024-09-11 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emkopo_api", "0003_rename_requesttype_apirequest_requestkind_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="apirequest",
            name="RequestKind",
        ),
        migrations.RemoveField(
            model_name="historicalapirequest",
            name="RequestKind",
        ),
        migrations.AddField(
            model_name="apirequest",
            name="RequestType",
            field=models.CharField(
                choices=[("inward", "INWARD"), ("outward", "OUTWARD")],
                default="",
                max_length=45,
                verbose_name="Request Type",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalapirequest",
            name="RequestType",
            field=models.CharField(
                choices=[("inward", "INWARD"), ("outward", "OUTWARD")],
                default="",
                max_length=45,
                verbose_name="Request Type",
            ),
            preserve_default=False,
        ),
    ]