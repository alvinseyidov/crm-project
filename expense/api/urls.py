from django.urls import path, include

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseCategoryViewSet, ExpenseViewSet

router = DefaultRouter()
router.register(r'expense-categories', ExpenseCategoryViewSet, basename='expensecategory')
router.register(r'expenses', ExpenseViewSet, basename='expense')
app_name = 'expense-api'
urlpatterns = [
    path('', include(router.urls)),
]

