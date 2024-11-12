import random
from django.core.management.base import BaseCommand
from catalog.models import Product
from organization.models import Organization
from core.models import Address
from sale.models import Customer, SalesOrder, SalesOrderItem
from accounting.models import Tax
from datetime import date, timedelta
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Generate dummy data for the sales module'

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
            self.stdout.write(self.style.WARNING('No taxes found in the database. Sales orders will have no tax applied.'))

        organizations = Organization.objects.all()
        addresses = Address.objects.all()
        products = Product.objects.all()
        taxes = Tax.objects.all() if Tax.objects.exists() else None

        # Generate dummy customers
        customers = []
        for i in range(5):
            customer = Customer.objects.create(
                organization=random.choice(organizations),
                name=f'Dummy Customer {i + 1}',
                email=f'dummy_customer_{i + 1}@example.com',
                phone=f'+123456789{i}',
                address=random.choice(addresses),
                contact_person=f'Contact Person {i + 1}'
            )
            customers.append(customer)
            self.stdout.write(self.style.SUCCESS(f'Created Customer: {customer.name}'))

        # Generate dummy sales orders
        for i in range(20):
            customer = random.choice(customers)
            organization = customer.organization
            order_number = f'SO-{i + 1:04d}-{get_random_string(6).upper()}'  # Generates a unique order number
            sales_order = SalesOrder.objects.create(
                organization=organization,
                customer=customer,
                order_number=order_number,
                date=date.today() - timedelta(days=random.randint(1, 30)),
                delivery_date=date.today() + timedelta(days=random.randint(1, 15)),
                status=random.choice(['draft', 'confirmed', 'shipped']),
                total_amount=0.0,  # Will calculate later
                tax_amount=0.0,  # Will calculate later
                grand_total=0.0  # Will calculate later
            )

            # Generate random sales order items
            total_amount = 0
            tax_amount = 0
            for _ in range(random.randint(1, 5)):  # Add 1 to 5 items per sales order
                product = random.choice(products)
                quantity = random.randint(1, 10)
                price_per_unit = random.uniform(50.0, 500.0)
                tax = random.choice(taxes) if taxes else None
                discount_percentage = random.uniform(0, 15)

                sales_order_item = SalesOrderItem.objects.create(
                    sales_order=sales_order,
                    product=product,
                    quantity=quantity,
                    price_per_unit=price_per_unit,
                    discount_percentage=discount_percentage,
                    tax=tax
                )
                total_item_price = sales_order_item.total_price
                total_amount += total_item_price
                if tax:
                    tax_amount += total_item_price * (tax.percent / 100)

            sales_order.total_amount = total_amount
            sales_order.tax_amount = tax_amount
            sales_order.grand_total = total_amount + tax_amount
            sales_order.save()

            self.stdout.write(self.style.SUCCESS(f'Created Sales Order: {sales_order.order_number} with {sales_order.sales_order_items.count()} items'))

        self.stdout.write(self.style.SUCCESS('Dummy data for Sales module generated successfully!'))
