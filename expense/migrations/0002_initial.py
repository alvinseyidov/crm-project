# Generated by Django 4.2.9 on 2024-11-09 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('expense', '0001_initial'),
        ('organization', '0001_initial'),
        ('purchase', '0001_initial'),
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensecategory',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_categories', to='organization.organization'),
        ),
        migrations.AddField(
            model_name='expense',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='expense.expensecategory'),
        ),
        migrations.AddField(
            model_name='expense',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='organization.organization'),
        ),
        migrations.AddField(
            model_name='expense',
            name='purchase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expenses', to='purchase.purchase', verbose_name='Related Purchase'),
        ),
        migrations.AddField(
            model_name='expense',
            name='sales_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expenses', to='sale.salesorder', verbose_name='Related Sales Order'),
        ),
    ]
