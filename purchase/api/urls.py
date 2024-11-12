from django.urls import path
from .views import (
    VendorListCreateView,
    VendorRetrieveUpdateDestroyView,
    PurchaseListCreateView,
    PurchaseRetrieveUpdateDestroyView,
    PurchaseItemListCreateView,
    PurchaseItemRetrieveUpdateDestroyView, LandedCostListCreateView, LandedCostRetrieveUpdateDestroyView,
    PurchaseReceiveListCreateView, PurchaseReceiveRetrieveUpdateDestroyView, PurchaseReceiveItemListCreateView,
    PurchaseReceiveItemRetrieveUpdateDestroyView, PurchaseDocumentListCreateView, CheckPurchaseOrderAcceptabilityView
)
app_name = 'purchase-api'
urlpatterns = [
    # Vendor endpoints
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorRetrieveUpdateDestroyView.as_view(), name='vendor-detail'),

    # Purchase endpoints
    path('purchases/', PurchaseListCreateView.as_view(), name='purchase-list-create'),
    path('purchases/<int:pk>/', PurchaseRetrieveUpdateDestroyView.as_view(), name='purchase-detail'),

    # PurchaseItem endpoints (optional)
    path('purchase-items/', PurchaseItemListCreateView.as_view(), name='purchaseitem-list-create'),
    path('purchase-items/<int:pk>/', PurchaseItemRetrieveUpdateDestroyView.as_view(), name='purchaseitem-detail'),

    path('landed-costs/', LandedCostListCreateView.as_view(), name='landed-costs-list-create'),
    path('landed-costs/<int:pk>/', LandedCostRetrieveUpdateDestroyView.as_view(), name='landed-costs-detail'),

    # PurchaseReceive endpoints
    path('purchase-receives/', PurchaseReceiveListCreateView.as_view(), name='purchase-receive-list-create'),
    path('purchase-receives/<int:pk>/', PurchaseReceiveRetrieveUpdateDestroyView.as_view(), name='purchase-receive-detail'),

    # PurchaseReceiveItem endpoints
    path('purchase-receive-items/', PurchaseReceiveItemListCreateView.as_view(), name='purchase-receive-item-list-create'),
    path('purchase-receive-items/<int:pk>/', PurchaseReceiveItemRetrieveUpdateDestroyView.as_view(), name='purchase-receive-item-detail'),


    path('documents/', PurchaseDocumentListCreateView.as_view(), name='purchase-documents-list-create'),

    path('check-purchase-order/', CheckPurchaseOrderAcceptabilityView.as_view(), name='check-purchase-order')
]
