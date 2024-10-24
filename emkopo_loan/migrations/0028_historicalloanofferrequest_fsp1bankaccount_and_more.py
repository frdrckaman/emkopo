# Generated by Django 5.1 on 2024-09-25 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emkopo_loan", "0027_alter_historicalloanofferrequest_emailaddress_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalloanofferrequest",
            name="FSP1BankAccount",
            field=models.CharField(
                blank=True, max_length=20, null=True, verbose_name="FSP1 Bank Account"
            ),
        ),
        migrations.AddField(
            model_name="historicalloanofferrequest",
            name="FSP1BankAccountName",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="FSP1 Bank Account Name"
            ),
        ),
        migrations.AddField(
            model_name="historicalloanofferrequest",
            name="FSP1Code",
            field=models.CharField(
                blank=True, max_length=8, null=True, verbose_name="FSP1 Code"
            ),
        ),
        migrations.AddField(
            model_name="historicalloanofferrequest",
            name="FSP1EndDate",
            field=models.DateTimeField(blank=True, null=True, verbose_name="FSP1 End Date"),
        ),
        migrations.AddField(
            model_name="historicalloanofferrequest",
            name="FSP1FinalPaymentDate",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="FSP1 Final Payment Date"
            ),
        ),
        migrations.AddField(
            model_name="historicalloanofferrequest",
            name="FSP1LastDeductionDate",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="FSP1 Last Deduction"
            ),
        ),
        migrations.AddField(
            model_name="historicalloanofferrequest",
            name="FSP1LoanNumber",
            field=models.CharField(
                blank=True, max_length=8, null=True, verbose_name="FSP1 Loan Number"
            ),
        ),
        migrations.AddField(
            model_name="historicalloanofferrequest",
            name="FSP1MNOChannels",
            field=models.CharField(
                blank=True, max_length=20, null=True, verbose_name="FSP1 MNO Channels"
            ),
        ),
        migrations.AddField(
            model_name="historicalloanofferrequest",
            name="FSP1PaymentReferenceNumber",
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                verbose_name="FSP1 Payment Reference Number",
            ),
        ),
        migrations.AddField(
            model_name="historicalloanofferrequest",
            name="FSP1SWIFTCode",
            field=models.CharField(
                blank=True, max_length=20, null=True, verbose_name="FSP1 SWIFT Code"
            ),
        ),
        migrations.AddField(
            model_name="historicalloanofferrequest",
            name="TakeOverBalance",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=40,
                null=True,
                verbose_name="Take over balance",
            ),
        ),
        migrations.AddField(
            model_name="loanofferrequest",
            name="FSP1BankAccount",
            field=models.CharField(
                blank=True, max_length=20, null=True, verbose_name="FSP1 Bank Account"
            ),
        ),
        migrations.AddField(
            model_name="loanofferrequest",
            name="FSP1BankAccountName",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="FSP1 Bank Account Name"
            ),
        ),
        migrations.AddField(
            model_name="loanofferrequest",
            name="FSP1Code",
            field=models.CharField(
                blank=True, max_length=8, null=True, verbose_name="FSP1 Code"
            ),
        ),
        migrations.AddField(
            model_name="loanofferrequest",
            name="FSP1EndDate",
            field=models.DateTimeField(blank=True, null=True, verbose_name="FSP1 End Date"),
        ),
        migrations.AddField(
            model_name="loanofferrequest",
            name="FSP1FinalPaymentDate",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="FSP1 Final Payment Date"
            ),
        ),
        migrations.AddField(
            model_name="loanofferrequest",
            name="FSP1LastDeductionDate",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="FSP1 Last Deduction"
            ),
        ),
        migrations.AddField(
            model_name="loanofferrequest",
            name="FSP1LoanNumber",
            field=models.CharField(
                blank=True, max_length=8, null=True, verbose_name="FSP1 Loan Number"
            ),
        ),
        migrations.AddField(
            model_name="loanofferrequest",
            name="FSP1MNOChannels",
            field=models.CharField(
                blank=True, max_length=20, null=True, verbose_name="FSP1 MNO Channels"
            ),
        ),
        migrations.AddField(
            model_name="loanofferrequest",
            name="FSP1PaymentReferenceNumber",
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                verbose_name="FSP1 Payment Reference Number",
            ),
        ),
        migrations.AddField(
            model_name="loanofferrequest",
            name="FSP1SWIFTCode",
            field=models.CharField(
                blank=True, max_length=20, null=True, verbose_name="FSP1 SWIFT Code"
            ),
        ),
        migrations.AddField(
            model_name="loanofferrequest",
            name="TakeOverBalance",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=40,
                null=True,
                verbose_name="Take over balance",
            ),
        ),
    ]
