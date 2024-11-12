from django.db import models
from django.conf import settings

class Country(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(
        "Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cities"
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Address(models.Model):
    city = models.ForeignKey(
        "City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="addresses"
    )
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Latitude
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Longitude
    postcode = models.CharField(max_length=20, blank=True, null=True)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.line1}, {self.line2 if self.line2 else ''}, {self.city.name if self.city else ''}, {self.city.country.name if self.city and self.city.country else ''}"
    
class Phone(models.Model):
    ext = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20)
    type = models.CharField(max_length=50, choices=[('M', 'Mobil'), ('E', 'Ev'), ('İ', 'İş')], blank=True, null=True)

    def __str__(self):
        return f"{self.phone} ({self.get_type_display()})"
    
class Currency(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)
    symbol = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"
    
class CurrencyRate(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='currency_rates'
    )
    from_currency = models.ForeignKey(
        'Currency', 
        on_delete=models.CASCADE,
        related_name='currency_rates_from'
    )
    to_currency = models.ForeignKey(
        'Currency',
        on_delete=models.CASCADE,
        related_name='currency_rates_to'
    )
    rate = models.DecimalField(
        max_digits=10,
        decimal_places=4,
    )
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rate from {self.from_currency} to {self.to_currency} on {self.date}"
