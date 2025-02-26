# Generated by Django 4.2.9 on 2024-11-09 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('check_in_time', models.TimeField()),
                ('check_out_time', models.TimeField(blank=True, null=True)),
                ('hours_worked', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type', models.CharField(choices=[('ANNUAL', 'Annual Leave'), ('SICK', 'Sick Leave'), ('UNPAID', 'Unpaid Leave'), ('MATERNITY', 'Maternity Leave')], max_length=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('HR', 'Human Resources'), ('AC', 'Accountant'), ('MG', 'Manager'), ('SP', 'Sales Person'), ('OT', 'Other')], max_length=2)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('hours_worked', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('tasks_completed', models.IntegerField(default=0)),
                ('payroll', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('employment_status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=10)),
                ('has_system_access', models.BooleanField(default=False)),
            ],
        ),
    ]
