# Generated by Django 4.2.9 on 2024-11-09 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounting', '0001_initial'),
        ('hr', '0001_initial'),
        ('purchase', '0001_initial'),
        ('sale', '0001_initial'),
        ('expense', '0001_initial'),
        ('organization', '0001_initial'),
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxdepositaccount',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tax_deposit_accounts', to='organization.organization', verbose_name='Organization'),
        ),
        migrations.AddField(
            model_name='tax',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taxes', to='organization.organization'),
        ),
        migrations.AddField(
            model_name='salesinvoicepayment',
            name='bank_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.bankaccount', verbose_name='Bank Account'),
        ),
        migrations.AddField(
            model_name='salesinvoicepayment',
            name='cash_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.cashaccount', verbose_name='Cash Account'),
        ),
        migrations.AddField(
            model_name='salesinvoicepayment',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_invoice_payments', to='organization.organization', verbose_name='Organization'),
        ),
        migrations.AddField(
            model_name='salesinvoicepayment',
            name='sales_invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='sale.salesinvoice', verbose_name='Sales Invoice'),
        ),
        migrations.AddField(
            model_name='purchasebillpayment',
            name='bank_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.bankaccount', verbose_name='Bank Account'),
        ),
        migrations.AddField(
            model_name='purchasebillpayment',
            name='cash_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.cashaccount', verbose_name='Cash Account'),
        ),
        migrations.AddField(
            model_name='purchasebillpayment',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_bill_payments', to='organization.organization', verbose_name='Organization'),
        ),
        migrations.AddField(
            model_name='purchasebillpayment',
            name='purchase_bill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bill_payments', to='purchase.bill', verbose_name='Purchase Bill'),
        ),
        migrations.AddField(
            model_name='fixedassetspurchaseinvoicepayment',
            name='bank_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.bankaccount', verbose_name='Bank Account'),
        ),
        migrations.AddField(
            model_name='fixedassetspurchaseinvoicepayment',
            name='cash_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.cashaccount', verbose_name='Cash Account'),
        ),
        migrations.AddField(
            model_name='fixedassetspurchaseinvoicepayment',
            name='fixed_assets_purchase_invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='assets.fixedassetspurchaseinvoice', verbose_name='Fixed Assets Purchase Invoice'),
        ),
        migrations.AddField(
            model_name='fixedassetspurchaseinvoicepayment',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixed_assets_purchase_invoice_payments', to='organization.organization', verbose_name='Organization'),
        ),
        migrations.AddField(
            model_name='expensepayment',
            name='bank_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.bankaccount', verbose_name='Bank Account'),
        ),
        migrations.AddField(
            model_name='expensepayment',
            name='cash_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.cashaccount', verbose_name='Cash Account'),
        ),
        migrations.AddField(
            model_name='expensepayment',
            name='expense',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='expense.expense', verbose_name='Expense'),
        ),
        migrations.AddField(
            model_name='cashaccount',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_accounts', to='organization.organization', verbose_name='Organization'),
        ),
        migrations.AddField(
            model_name='cashaccount',
            name='responsible_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.worker', verbose_name='Responsible Person'),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_accounts', to='organization.organization', verbose_name='Organization'),
        ),
    ]
