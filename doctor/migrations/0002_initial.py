# Generated by Django 4.2.9 on 2024-11-09 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_initial'),
        ('organization', '0001_initial'),
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='zone',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization'),
        ),
        migrations.AddField(
            model_name='hospital',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospitals', to='organization.organization'),
        ),
        migrations.AddField(
            model_name='hospital',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospitals', to='doctor.zone'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='doctor.branch'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='core.city'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='doctor.hospital'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='organization.organization'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='doctor.zone'),
        ),
        migrations.AddField(
            model_name='branch',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization'),
        ),
    ]
