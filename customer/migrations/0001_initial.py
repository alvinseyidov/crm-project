# Generated by Django 4.2.9 on 2024-11-09 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_person', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('tin', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('logo_image', models.ImageField(blank=True, null=True, upload_to='customer_logos/')),
                ('industry', models.CharField(blank=True, max_length=255, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('customer_since', models.DateField(blank=True, null=True)),
                ('last_contacted', models.DateTimeField(blank=True, null=True)),
                ('preferred_contact_method', models.CharField(choices=[('email', 'Email'), ('phone', 'Phone'), ('other', 'Other')], default='email', max_length=50)),
                ('customer_type', models.CharField(choices=[('lead', 'Lead'), ('prospect', 'Prospect'), ('client', 'Client')], default='client', max_length=50)),
                ('lifetime_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('recent_purchase_date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
