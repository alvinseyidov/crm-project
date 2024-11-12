# Generated by Django 4.2.9 on 2024-11-09 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounting', '0001_initial'),
        ('hr', '0001_initial'),
        ('catalog', '0001_initial'),
        ('customer', '0001_initial'),
        ('organization', '0001_initial'),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=255, unique=True)),
                ('date', models.DateField()),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('shipped', 'Shipped'), ('canceled', 'Canceled')], default='draft', max_length=20)),
                ('payment_status', models.CharField(choices=[('invoiced', 'Invoiced'), ('paid', 'Paid'), ('partial_paid', 'Partial Paid')], default='invoiced', max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('tax_amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization')),
                ('salesperson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.worker', verbose_name='Salesperson')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_sales', to='inventory.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='SalesReturnOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_number', models.CharField(max_length=255, unique=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('confirmed', 'Confirmed'), ('processed', 'Processed'), ('canceled', 'Canceled')], default='draft', max_length=20)),
                ('reason', models.TextField(blank=True, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('tax_amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sales_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='return_orders', to='sale.salesorder')),
            ],
        ),
        migrations.CreateModel(
            name='SalesReturnOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=12)),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=12)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('tax_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product')),
                ('return_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='return_order_items', to='sale.salesreturnorder')),
                ('tax', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.tax')),
            ],
        ),
        migrations.CreateModel(
            name='SalesOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=12)),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=12)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('tax_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('discount_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_order_items', to='catalog.product')),
                ('sales_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_order_items', to='sale.salesorder')),
                ('tax', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.tax')),
            ],
        ),
        migrations.CreateModel(
            name='SalesInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=20, verbose_name='Invoice Number')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total Amount')),
                ('paid_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Paid Amount')),
                ('remaining_balance', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Remaining Balance')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('issued', 'Issued'), ('partially_paid', 'Partially Paid'), ('paid', 'Paid'), ('overdue', 'Overdue')], default='draft', max_length=20, verbose_name='Status')),
                ('issued_date', models.DateField(blank=True, null=True, verbose_name='Issued Date')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='Due Date')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_invoices', to='customer.customer', verbose_name='Customer')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_invoices', to='organization.organization', verbose_name='Organization')),
                ('sales_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='sale.salesorder', verbose_name='Sales Order')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
