from rest_framework import serializers
from expense.models import Expense, ExpenseCategory
from django.contrib.auth import get_user_model
User = get_user_model()


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'organization', 'name', 'description']


class ExpenseUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]
class ExpenseSerializer(serializers.ModelSerializer):
    user_position = serializers.SerializerMethodField()

    def get_user_position(self, expense, *args, **kwargs):
        try:
            return expense.user.organizations.get(organization=expense.organization).position.name
        except:
            return '-'

    user = ExpenseUserSerializer()
    category = ExpenseCategorySerializer()
    class Meta:
        model = Expense
        fields = [
            'id', 'organization', 'user', 'category', 'amount', 'receipt',
            'description', 'date', 'status', 'submitted_at', 'approved_at',
            'rejected_at', 'paid_at', 'created_at', 'updated_at','user_position'
        ]
