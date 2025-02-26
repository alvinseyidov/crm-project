# Generated by Django 4.2.9 on 2024-11-09 14:52

from django.db import migrations, models
import expense.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_type', models.CharField(choices=[('operational', 'Operational'), ('administrative', 'Administrative'), ('purchase_related', 'Purchase Related'), ('sales_related', 'Sales Related'), ('other', 'Other')], default='other', max_length=20, verbose_name='Expense Type')),
                ('currency', models.CharField(choices=[('USD', 'US Dollar'), ('EUR', 'Euro'), ('RUB', 'Russian Ruble'), ('AZN', 'Azerbaijani Manat'), ('TL', 'Turkish Lira')], default='AZN', max_length=3, verbose_name='Currency')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('receipt', models.ImageField(blank=True, null=True, upload_to='receipts/', validators=[expense.models.validate_receipt_size])),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('submitted', 'Submitted'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected'), ('paid', 'Paid')], default='submitted', max_length=20)),
                ('submitted_at', models.DateTimeField(blank=True, null=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('rejected_at', models.DateTimeField(blank=True, null=True)),
                ('paid_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('date',),
            },
        ),
        migrations.CreateModel(
            name='ExpenseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
