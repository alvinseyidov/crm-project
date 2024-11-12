from rest_framework import serializers
from customer.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'organization', 'name', 'email', 'phone', 'address', 'tin', 'contact_person', 'description',
                  'logo_image', 'is_active', 'created_at', 'updated_at']
