import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

from accounting.models import Tax
from .managers import ProductManager
import requests


def validate_image(image):
    max_size = 2 * 1024 * 1024  # 2 MB
    if image.size > max_size:
        raise ValidationError("Image file too large (max 2 MB)")


class Manufacturer(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='manufacturers'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Manufacturer"
        verbose_name_plural = "Manufacturers"
        unique_together = ('organization', 'name')
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f'{self.organization.name} - {self.name}'

    def get_display_name(self, show_organization=True):
        if show_organization:
            return f'{self.organization.name} - {self.name}'
        return self.name

class Brand(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='brands'
    )
    name = models.CharField(max_length=256)
    logo = models.ImageField(upload_to='brand_logos/',null=True, blank=True, validators=[validate_image])
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        unique_together = ('organization', 'name')
        indexes = [
            models.Index(fields=['name']),
        ]


    def __str__(self):
        return f'{self.organization.name} - {self.name}'

    def get_display_name(self, show_organization=True):
        if show_organization:
            return f'{self.organization.name} - {self.name}'
        return self.name


class Category(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='organization_categories'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    name = models.CharField(max_length=255, db_index=True)  # Index for performance on searches
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='category_images/',validators=[validate_image])

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('organization', 'name')
        verbose_name_plural = 'categories'  # Makes it plural in admin panel
        ordering = ['name']  # Default ordering by name
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
        ]

    def validate_image(image):
        max_size = 2 * 1024 * 1024  # 2 MB
        if image.size > max_size:
            raise ValidationError("Image file too large (max 2 MB)")

    def __str__(self):
        return f"{self.organization.name}-{self.name} (Parent: {self.parent.name if self.parent else 'None'})"

    def get_full_path(self, separator=" > "):
        if self.parent:
            return f"{self.parent.get_full_path(separator)}{separator}{self.name}"
        return self.name

    def get_ancestors(self):
        ancestors = []
        parent = self.parent
        while parent:
            ancestors.append(parent)
            parent = parent.parent
        return ancestors[::-1]  # Return in top-down order

    @property
    def children(self):
        return self.subcategories.all()

    def has_children(self):
        return self.subcategories.exists()


class ProductAttribute(models.Model):
    """
    Product attributes define customizable properties such as color, size, material, etc.
    """
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='product_attributes'
    )
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('organization', 'name')

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('attribute', 'value')

    @property
    def organization(self):
        # Return the organization from the related attribute
        return self.attribute.organization

    def __str__(self):
        return f'{self.attribute.name}: {self.value}'


class Product(models.Model):
    PRODUCT_TYPE = [
        ('consumable', 'İstifadə üçün'),
        ('service', 'Xidmət'),
        ('product', 'Məhsul'),
        ('raw_material', 'Xammal'),
        ('agriculture', 'Kənd təsərrüfat məhsulu'),
    ]
    PRODUCT_MEASUREMENT = [
        ('pc', 'ədəd'),
        ('box', 'qutu'),
        ('kg', 'kq'),
        ('lt', 'lt'),
        ('ml', 'ml'),
        ('qr', 'qr'),
        ('m', 'm'),
        ('cm', 'sm'),
    ]

    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='products'
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET, null=True, blank=True, related_name="products")
    measurement = models.CharField(max_length=100, choices=PRODUCT_MEASUREMENT, default="pc")
    type = models.CharField(max_length=100, choices=PRODUCT_TYPE, default="product")
    attributes = models.ManyToManyField(ProductAttributeValue, blank=True, related_name='products')
    average_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.ForeignKey(
        'accounting.Tax',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sku', 'organization'], name='unique_sku_per_organization'),
        ]
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['is_active', 'is_deleted']),
            models.Index(fields=['barcode'], name='barcode_idx'),
            models.Index(fields=['organization'], name='organization_idx'),
        ]

    def __str__(self):
        return self.name

    def update_average_cost(self, new_cost, quantity):
        current_total_value = self.average_cost * self.current_stock_quantity
        new_total_value = current_total_value + (new_cost * quantity)
        self.average_cost = new_total_value / (self.current_stock_quantity + quantity)
        self.save()

    def is_trade_margin(self):
        return self.type == 'agriculture'

    def clean(self):
        """
        Ensure barcode is unique per organization when provided.
        """
        if self.barcode:  # Only validate if barcode is not None or empty
            if Product.objects.filter(barcode=self.barcode, organization=self.organization).exclude(
                    id=self.id).exists():
                raise ValidationError("This barcode is already used for this organization.")

    def get_first_image(self, request):
        if self.images.exists():
            first_image = self.images.first()
            return request.build_absolute_uri(first_image.image.url)
        return request.build_absolute_uri('/static/images/placeholder.png')

    @property
    def cost(self):
        # Return the most recent cost of the product
        latest_cost = self.costs.order_by('-date', '-id').first()
        return latest_cost.amount if latest_cost else 0

    @property
    def price(self):
        # Return the most recent price of the product
        latest_price = self.prices.order_by('-date', '-id').first()
        return latest_price.amount if latest_price else 0

    @property
    def stock(self):
        # Calculate stock based on related stock movements (not yet implemented)
        return 0

    def save(self, *args, **kwargs):
        if not self.tax:
            default_tax, created = Tax.objects.get_or_create(
                organization=self.organization,
                percent=0,
                defaults={'name': "ƏDV'siz"}
            )
            self.tax = default_tax
        if not self.category:
            default_category, created = Category.objects.get_or_create(
                name="Uncategorized",
                organization=self.organization
            )
            self.category = default_category
        self.clean()
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='product_images/',validators=[validate_image])
    sorting = models.IntegerField(default=0)

    class Meta:
        ordering = ('sorting','id')

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductCost(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='costs'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    date = models.DateField()
    vendor = models.ForeignKey("purchase.Vendor", on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="product_costs")

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return f"Cost for {self.product.name} on {self.date}"


class ProductPrice(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='prices'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    date = models.DateField()

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return f"Price for {self.product.name} on {self.date}"


class ProductCostHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase = models.ForeignKey('purchase.Purchase', on_delete=models.SET_NULL, null=True)
    cost_date = models.DateField(auto_now_add=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    landed_cost = models.DecimalField(max_digits=10, decimal_places=2)  # Total landed cost per unit
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)  # Final cost per unit with landed costs

    def save_history(self, purchase_item):
        self.product = purchase_item.product
        self.purchase = purchase_item.purchase
        self.unit_cost = purchase_item.unit_cost
        self.landed_cost = purchase_item.allocated_landed_cost / purchase_item.quantity
        self.total_cost = self.unit_cost + self.landed_cost
        self.save()
