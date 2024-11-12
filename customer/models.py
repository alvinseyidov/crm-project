from django.db import models

class Customer(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    tin = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo_image = models.ImageField(upload_to='customer_logos/', blank=True, null=True)

    # New CRM-related fields
    industry = models.CharField(max_length=255, blank=True, null=True)  # Industry sector of the customer
    website = models.URLField(blank=True, null=True)  # Customer website
    customer_since = models.DateField(null=True, blank=True)  # Date when the customer relationship started

    # Communication and interactions
    last_contacted = models.DateTimeField(null=True, blank=True)  # Last interaction with the customer
    preferred_contact_method = models.CharField(max_length=50,
                                                choices=[('email', 'Email'), ('phone', 'Phone'), ('other', 'Other')],
                                                default='email')

    # CRM status and categorization
    customer_type = models.CharField(max_length=50,
                                     choices=[('lead', 'Lead'), ('prospect', 'Prospect'), ('client', 'Client')],
                                     default='client')


    # Sales data and revenue tracking
    lifetime_value = models.DecimalField(max_digits=12, decimal_places=2,
                                         default=0.0)  # Total revenue from this customer
    recent_purchase_date = models.DateField(null=True, blank=True)  # Date of the most recent purchase

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
