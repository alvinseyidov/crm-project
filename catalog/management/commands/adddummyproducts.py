from django.core.management.base import BaseCommand
from catalog.models import Product, Brand, Category, ProductPrice, ProductCost, ProductMeasurement
import random
from datetime import date


class Command(BaseCommand):
    help = 'Generate dummy products'

    def handle(self, *args, **kwargs):
        brands = Brand.objects.all()
        categories = Category.objects.all()

        def generate_price():
            return round(random.uniform(100, 1000), 2)

        for i in range(25):
            brand = random.choice(brands)
            category = random.choice(categories)
            product_measurement = ProductMeasurement.objects.first()
            product = Product.objects.create(
                organization_id=1,
                name=f'Dummy Product {i + 1}',
                sku=f'SKU-{i + 1:03d}',
                barcode=f'BARCODE-{i + 1:06d}',
                brand=brand,
                product_type='consumable',
                is_active=True,
                product_measurement=product_measurement,
            )

            product.categories.add(category)

            ProductPrice.objects.create(
                product=product,
                amount=generate_price(),
                date=date.today()
            )

            ProductCost.objects.create(
                product=product,
                amount=generate_price(),
                date=date.today()
            )

            self.stdout.write(self.style.SUCCESS(f'Created {product.name}'))
