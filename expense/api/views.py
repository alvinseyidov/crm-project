from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from expense.models import Expense, ExpenseCategory
from .serializers import ExpenseSerializer, ExpenseCategorySerializer
from rest_framework.permissions import IsAuthenticated

class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = ExpenseCategory.objects.all()  # Explicitly define queryset

    def get_queryset(self):
        user = self.request.user
        return ExpenseCategory.objects.filter(organization__organization_users__user=user)


class ExpenseViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Expense.objects.all()  # Explicitly define queryset

    def get_queryset(self):
        user = self.request.user
        return Expense.objects.filter(organization__organization_users__user=user)

