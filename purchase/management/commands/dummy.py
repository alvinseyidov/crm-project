import random
from django.core.management.base import BaseCommand
from catalog.models import Product
from organization.models import Organization
from core.models import Address
from purchase.models import Vendor, Purchase, PurchaseItem
from accounting.models import Tax
from datetime import date, timedelta
from django.utils.crypto import get_random_string  # Import this for generating unique strings

class Command(BaseCommand):
    help = 'Generate dummy data for the purchase module'

    def handle(self, *args, **kwargs):
        # Ensure there are existing products, organizations, and addresses
        if not Product.objects.exists():
            self.stdout.write(self.style.ERROR('You must have at least one Product in the database.'))
            return
        if not Organization.objects.exists():
            self.stdout.write(self.style.ERROR('You must have at least one Organization in the database.'))
            return
        if not Address.objects.exists():
            self.stdout.write(self.style.ERROR('You must have at least one Address in the database.'))
            return

        # Set optional check for taxes
        if not Tax.objects.exists():
            self.stdout.write(self.style.WARNING('No taxes found in the database. Purchases will have no tax applied.'))

        organizations = Organization.objects.all()
        addresses = Address.objects.all()
        products = Product.objects.all()
        taxes = Tax.objects.all() if Tax.objects.exists() else None

        # Generate dummy vendors
        vendors = []
        for i in range(5):
            vendor = Vendor.objects.create(
                organization=random.choice(organizations),
                name=f'Dummy Vendor {i + 1}',
                email=f'dummy_vendor_{i + 1}@example.com',
                phone=f'+123456789{i}',
                address=random.choice(addresses),
                tin=f'123456789{i}',
                contact_person=f'Contact Person {i + 1}'
            )
            vendors.append(vendor)
            self.stdout.write(self.style.SUCCESS(f'Created Vendor: {vendor.name}'))

        # Generate dummy purchase orders
        for i in range(20):
            vendor = random.choice(vendors)
            organization = vendor.organization
            # Ensure unique order number by appending a random string
            order_number = f'PO-{i + 1:04d}-{get_random_string(6).upper()}'  # Generates a unique order number
            purchase = Purchase.objects.create(
                organization=organization,
                vendor=vendor,
                order_number=order_number,
                date=date.today() - timedelta(days=random.randint(1, 30)),
                delivery_date=date.today() + timedelta(days=random.randint(1, 15)),
                status=random.choice(['draft', 'confirmed', 'received']),
                total_amount=0.0,  # Will calculate later
                tax_amount=0.0,  # Will calculate later
                grand_total=0.0  # Will calculate later
            )

            # Generate random purchase items
            total_amount = 0
            tax_amount = 0
            for _ in range(random.randint(1, 5)):  # Add 1 to 5 items per purchase
                product = random.choice(products)
                quantity = random.randint(1, 10)
                price_per_unit = random.uniform(50.0, 500.0)
                tax = random.choice(taxes) if taxes else None
                discount_percentage = random.uniform(0, 15)

                purchase_item = PurchaseItem.objects.create(
                    purchase=purchase,
                    product=product,
                    quantity=quantity,
                    price_per_unit=price_per_unit,
                    discount_percentage=discount_percentage,
                    tax=tax
                )
                total_item_price = purchase_item.total_price
                total_amount += total_item_price
                if tax:
                    tax_amount += total_item_price * (tax.percent / 100)

            purchase.total_amount = total_amount
            purchase.tax_amount = tax_amount
            purchase.grand_total = total_amount + tax_amount
            purchase.save()

            self.stdout.write(self.style.SUCCESS(f'Created Purchase: {purchase.order_number} with {purchase.purchase_items.count()} items'))

        self.stdout.write(self.style.SUCCESS('Dummy data for Purchase module generated successfully!'))
