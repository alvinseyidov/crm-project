from rest_framework import generics, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from catalog.models import (
    Category, Brand, ProductAttribute, ProductAttributeValue,
    Product, ProductImage, ProductCost, ProductPrice, Manufacturer
)
from .serializers import (
    CategoryDetailSerializer, CategoryListSerializer, CategoryCreateSerializer, BrandSerializer,
    ProductAttributeSerializer, ProductAttributeValueSerializer,
    ProductListSerializer, ProductImageSerializer, ProductCostSerializer,
    ProductPriceSerializer, ProductDetailSerializer, ProductCreateSerializer,
    ManufacturerSerializer,
)


# Base class for views to handle common organization filtering
class OrganizationFilteredView(generics.GenericAPIView):
    """
    Base view that filters queryset based on an organization ID provided in the query parameters.
    """

    def get_queryset(self):
        org_id = self.request.query_params.get('org_id')

        # If org_id is required and missing, raise an error
        if not org_id:
            raise exceptions.ValidationError("Organization ID (org_id) is required.")

        # Filter by organization if org_id is provided
        return self.queryset.filter(organization__id=org_id)


# Brand Views
class BrandListCreateView(OrganizationFilteredView, generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class BrandRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


# Manufacturer Views
class ManufacturerListCreateView(OrganizationFilteredView, generics.ListCreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ManufacturerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


# Category Views
class CategoryListView(OrganizationFilteredView, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


# Product Attribute Views
class ProductAttributeListCreateView(OrganizationFilteredView, generics.ListCreateAPIView):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ProductAttributeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


# Product Attribute Value Views
class ProductAttributeValueListCreateView(generics.ListCreateAPIView):
    queryset = ProductAttributeValue.objects.all()
    serializer_class = ProductAttributeValueSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ProductAttributeValueRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductAttributeValue.objects.all()
    serializer_class = ProductAttributeValueSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


# Product Views
class ProductListView(OrganizationFilteredView, generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]



class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


# Product Image Views
class ProductImageListCreateView(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ProductImageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


# Product Cost Views
class ProductCostListCreateView(generics.ListCreateAPIView):
    queryset = ProductCost.objects.all()
    serializer_class = ProductCostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ProductCostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCost.objects.all()
    serializer_class = ProductCostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


# Product Price Views
class ProductPriceListCreateView(generics.ListCreateAPIView):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ProductPriceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
