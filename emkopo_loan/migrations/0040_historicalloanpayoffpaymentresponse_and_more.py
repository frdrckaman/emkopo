# Generated by Django 5.1 on 2024-10-13 11:39

import _socket
import django.db.models.deletion
import django.utils.timezone
import django_audit_fields.fields.hostname_modification_field
import django_audit_fields.fields.userfield
import django_audit_fields.fields.uuid_auto_field
import django_audit_fields.models.audit_model_mixin
import django_revision.revision_field
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emkopo_loan", "0039_historicalloanrepaymentoffbalancerequest_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalLoanPayoffPaymentResponse",
            fields=[
                (
                    "revision",
                    django_revision.revision_field.RevisionField(
                        blank=True,
                        editable=False,
                        help_text="System field. Git repository tag:branch:commit.",
                        max_length=75,
                        null=True,
                        verbose_name="Revision",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "user_created",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user created",
                    ),
                ),
                (
                    "user_modified",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user modified",
                    ),
                ),
                (
                    "hostname_created",
                    models.CharField(
                        blank=True,
                        default=_socket.gethostname,
                        help_text="System field. (modified on create only)",
                        max_length=60,
                        verbose_name="Hostname created",
                    ),
                ),
                (
                    "hostname_modified",
                    django_audit_fields.fields.hostname_modification_field.HostnameModificationField(
                        blank=True,
                        help_text="System field. (modified on every save)",
                        max_length=50,
                        verbose_name="Hostname modified",
                    ),
                ),
                (
                    "device_created",
                    models.CharField(blank=True, max_length=10, verbose_name="Device created"),
                ),
                (
                    "device_modified",
                    models.CharField(
                        blank=True, max_length=10, verbose_name="Device modified"
                    ),
                ),
                (
                    "locale_created",
                    models.CharField(
                        blank=True,
                        help_text="Auto-updated by Modeladmin",
                        max_length=10,
                        null=True,
                        verbose_name="Locale created",
                    ),
                ),
                (
                    "locale_modified",
                    models.CharField(
                        blank=True,
                        help_text="Auto-updated by Modeladmin",
                        max_length=10,
                        null=True,
                        verbose_name="Locale modified",
                    ),
                ),
                (
                    "id",
                    django_audit_fields.fields.uuid_auto_field.UUIDAutoField(
                        blank=True,
                        db_index=True,
                        editable=False,
                        help_text="System auto field. UUID primary key.",
                    ),
                ),
                ("LoanNumber", models.CharField(max_length=20, verbose_name="Loan Number")),
                (
                    "TotalPayOffAmount",
                    models.CharField(max_length=30, verbose_name="First Name"),
                ),
                (
                    "LastDeductionDate",
                    models.DateTimeField(verbose_name="Last Deduction Date"),
                ),
                (
                    "FSPBankAccount",
                    models.CharField(max_length=45, verbose_name="FSP Bank Account"),
                ),
                (
                    "FSPBankAccountName",
                    models.CharField(max_length=250, verbose_name="FSP Bank Account Name"),
                ),
                ("SWIFTCode", models.CharField(max_length=45, verbose_name="Swift Code")),
                ("MNOChannels", models.CharField(max_length=45, verbose_name="MNO Channels")),
                ("FinalPaymentDate", models.DateTimeField(verbose_name="Final Payment Date")),
                ("EndDate", models.DateTimeField(verbose_name="End Date")),
                (
                    "Timestamp",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Timestamp"
                    ),
                ),
                ("status", models.IntegerField(default=1, verbose_name="Status")),
                ("MessageType", models.CharField(max_length=100, verbose_name="Message Type")),
                (
                    "RequestType",
                    models.CharField(
                        choices=[("incoming", "INCOMING"), ("outgoing", "OUTGOING")],
                        max_length=45,
                        verbose_name="Request Type",
                    ),
                ),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical Payoff Payment Response",
                "verbose_name_plural": "historical Payoff Payment Response",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="LoanPayoffPaymentResponse",
            fields=[
                (
                    "revision",
                    django_revision.revision_field.RevisionField(
                        blank=True,
                        editable=False,
                        help_text="System field. Git repository tag:branch:commit.",
                        max_length=75,
                        null=True,
                        verbose_name="Revision",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "user_created",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user created",
                    ),
                ),
                (
                    "user_modified",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user modified",
                    ),
                ),
                (
                    "hostname_created",
                    models.CharField(
                        blank=True,
                        default=_socket.gethostname,
                        help_text="System field. (modified on create only)",
                        max_length=60,
                        verbose_name="Hostname created",
                    ),
                ),
                (
                    "hostname_modified",
                    django_audit_fields.fields.hostname_modification_field.HostnameModificationField(
                        blank=True,
                        help_text="System field. (modified on every save)",
                        max_length=50,
                        verbose_name="Hostname modified",
                    ),
                ),
                (
                    "device_created",
                    models.CharField(blank=True, max_length=10, verbose_name="Device created"),
                ),
                (
                    "device_modified",
                    models.CharField(
                        blank=True, max_length=10, verbose_name="Device modified"
                    ),
                ),
                (
                    "locale_created",
                    models.CharField(
                        blank=True,
                        help_text="Auto-updated by Modeladmin",
                        max_length=10,
                        null=True,
                        verbose_name="Locale created",
                    ),
                ),
                (
                    "locale_modified",
                    models.CharField(
                        blank=True,
                        help_text="Auto-updated by Modeladmin",
                        max_length=10,
                        null=True,
                        verbose_name="Locale modified",
                    ),
                ),
                (
                    "id",
                    django_audit_fields.fields.uuid_auto_field.UUIDAutoField(
                        blank=True,
                        editable=False,
                        help_text="System auto field. UUID primary key.",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("LoanNumber", models.CharField(max_length=20, verbose_name="Loan Number")),
                (
                    "TotalPayOffAmount",
                    models.CharField(max_length=30, verbose_name="First Name"),
                ),
                (
                    "LastDeductionDate",
                    models.DateTimeField(verbose_name="Last Deduction Date"),
                ),
                (
                    "FSPBankAccount",
                    models.CharField(max_length=45, verbose_name="FSP Bank Account"),
                ),
                (
                    "FSPBankAccountName",
                    models.CharField(max_length=250, verbose_name="FSP Bank Account Name"),
                ),
                ("SWIFTCode", models.CharField(max_length=45, verbose_name="Swift Code")),
                ("MNOChannels", models.CharField(max_length=45, verbose_name="MNO Channels")),
                ("FinalPaymentDate", models.DateTimeField(verbose_name="Final Payment Date")),
                ("EndDate", models.DateTimeField(verbose_name="End Date")),
                (
                    "Timestamp",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Timestamp"
                    ),
                ),
                ("status", models.IntegerField(default=1, verbose_name="Status")),
                ("MessageType", models.CharField(max_length=100, verbose_name="Message Type")),
                (
                    "RequestType",
                    models.CharField(
                        choices=[("incoming", "INCOMING"), ("outgoing", "OUTGOING")],
                        max_length=45,
                        verbose_name="Request Type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Payoff Payment Response",
                "verbose_name_plural": "Payoff Payment Response",
                "abstract": False,
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "indexes": [
                    models.Index(
                        fields=["modified", "created"], name="emkopo_loan_modifie_eebad8_idx"
                    ),
                    models.Index(
                        fields=["user_modified", "user_created"],
                        name="emkopo_loan_user_mo_a18ae5_idx",
                    ),
                ],
            },
        ),
    ]
