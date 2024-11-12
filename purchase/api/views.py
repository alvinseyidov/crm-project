from django.db.models import Max
from rest_framework import serializers, generics, views, response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.schemas import views

from purchase.models import Vendor, Purchase, PurchaseItem, LandedCost, PurchaseReceive, PurchaseReceiveItem, \
    PurchaseDocument
from .serializers import VendorSerializer, PurchaseItemSerializer, LandedCostSerializer, PurchaseCreateSerializer, \
    PurchaseListSerializer, PurchaseDetailSerializer, PurchaseReceiveItemSerializer, \
    PurchaseReceiveItemDetailSerializer, PurchaseReceiveSerializer, PurchaseReceiveDetailSerializer, \
    PurchaseDocumentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication



# Vendor Views
class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter by organization via query param (org_id).
        """
        queryset = super().get_queryset()
        org_id = self.request.query_params.get('org_id')
        if org_id:
            queryset = queryset.filter(organization__id=org_id)
        return queryset

class VendorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]




# List and Create View
class LandedCostListCreateView(generics.ListCreateAPIView):
    queryset = LandedCost.objects.all()
    serializer_class = LandedCostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter by organization via query param (org_id).
        """
        queryset = super().get_queryset()
        org_id = self.request.query_params.get('org_id')
        if org_id:
            queryset = queryset.filter(organization__id=org_id)
        return queryset
    def perform_create(self, serializer):
        # Optionally, add custom behavior here if needed
        serializer.save()


# Retrieve, Update, and Delete View
class LandedCostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LandedCost.objects.all()
    serializer_class = LandedCostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

# Purchase Views


class PurchaseListCreateView(generics.ListCreateAPIView):
    queryset = Purchase.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PurchaseCreateSerializer
        return PurchaseListSerializer


    def get_queryset(self):
        """
        Optionally filter by organization and status via query params (org_id, status).
        """
        queryset = super().get_queryset()
        org_id = self.request.query_params.get('org_id')
        status = self.request.query_params.get('status')
        if org_id:
            queryset = queryset.filter(organization__id=org_id)
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class PurchaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Purchase.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PurchaseCreateSerializer  # Use the create serializer for updates
        return PurchaseDetailSerializer


# PurchaseItem Views (Optional: If needed separately)
class PurchaseItemListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter by purchase_id via query param.
        """
        queryset = super().get_queryset()
        purchase_id = self.request.query_params.get('purchase_id')
        if purchase_id:
            queryset = queryset.filter(purchase__id=purchase_id)
        return queryset

class PurchaseItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]







# PurchaseReceive Views
class PurchaseReceiveListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseReceive.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PurchaseReceiveSerializer
        return PurchaseReceiveDetailSerializer

    def get_queryset(self):
        """
        Optionally filter by organization and purchase via query params (org_id, purchase_id).
        """
        queryset = super().get_queryset()
        org_id = self.request.query_params.get('org_id')
        purchase_id = self.request.query_params.get('purchase_id')
        if org_id:
            queryset = queryset.filter(organization__id=org_id)
        if purchase_id:
            queryset = queryset.filter(purchase__id=purchase_id)
        return queryset


class PurchaseReceiveRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseReceive.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PurchaseReceiveSerializer  # Use the basic serializer for updates
        return PurchaseReceiveDetailSerializer

# PurchaseReceiveItem Views
class PurchaseReceiveItemListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseReceiveItem.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PurchaseReceiveItemSerializer
        return PurchaseReceiveItemDetailSerializer

    def get_queryset(self):
        """
        Optionally filter by purchase_receive via query param (purchase_receive_id).
        """
        queryset = super().get_queryset()
        purchase_receive_id = self.request.query_params.get('purchase_receive_id')
        if purchase_receive_id:
            queryset = queryset.filter(purchase_receive__id=purchase_receive_id)
        return queryset


class PurchaseReceiveItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseReceiveItem.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PurchaseReceiveItemSerializer  # Use the basic serializer for updates
        return PurchaseReceiveItemDetailSerializer



# Views
class PurchaseDocumentListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseDocument.objects.all()
    serializer_class = PurchaseDocumentSerializer



class PurchaseDocumentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseDocument.objects.all()
    serializer_class = PurchaseDocumentSerializer


# API View for Checking Purchase Order Acceptability
class CheckPurchaseOrderAcceptabilityView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        order_number = request.query_params.get('order_number')
        organization_id = request.query_params.get('organization_id')

        if not order_number or not organization_id:
            return response.Response({
                "error": "order_number and organization_id are required parameters."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if the order number is unique for the given organization
        exists = Purchase.objects.filter(order_number=order_number, organization_id=organization_id).exists()

        if exists:
            # Generate a recommended order number
            max_order_number = Purchase.objects.filter(organization_id=organization_id).aggregate(Max('order_number'))['order_number__max']
            recommended_order_number = self.generate_next_order_number(max_order_number)
            return response.Response({
                "acceptable": False,
                "message": "Order number already exists for this organization.",
                "recommended_order_number": recommended_order_number
            }, status=status.HTTP_200_OK)

        return response.Response({
            "acceptable": True,
            "message": "Order number is acceptable."
        }, status=status.HTTP_200_OK)

    def generate_next_order_number(self, current_max_order_number):
        if current_max_order_number and current_max_order_number.startswith("PO-"):
            current_number = int(current_max_order_number.split("PO-")[1])
            next_number = current_number + 1
            return f"PO-{str(next_number).zfill(6)}"
        else:
            return "PO-000001"
