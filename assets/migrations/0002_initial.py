# Generated by Django 4.2.9 on 2024-11-09 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
        ('purchase', '0001_initial'),
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixedassetspurchaseinvoice',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixed_assets_purchase_invoices', to='organization.organization', verbose_name='Organization'),
        ),
        migrations.AddField(
            model_name='fixedassetspurchaseinvoice',
            name='purchase_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='assets.fixedassetspurchase', verbose_name='Purchase Order'),
        ),
        migrations.AddField(
            model_name='fixedassetspurchaseinvoice',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixed_assets_purchase_invoices', to='purchase.vendor', verbose_name='Supplier'),
        ),
        migrations.AddField(
            model_name='fixedassetspurchase',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixed_asset_purchases', to='organization.organization'),
        ),
        migrations.AddField(
            model_name='fixedassetspurchase',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixed_asset_purchases', to='purchase.vendor'),
        ),
        migrations.AddField(
            model_name='fixedassetscategory',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixed_asset_categories', to='organization.organization'),
        ),
        migrations.AddField(
            model_name='fixedassets',
            name='asset_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.fixedassetscategory'),
        ),
        migrations.AddField(
            model_name='fixedassets',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixed_assets', to='organization.organization'),
        ),
    ]
