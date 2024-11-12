from django.urls import path
from .views import (
    CategoryListView, CategoryCreateView, CategoryRetrieveUpdateDestroyView,
    BrandListCreateView, BrandRetrieveUpdateDestroyView,
    ProductAttributeListCreateView, ProductAttributeRetrieveUpdateDestroyView,
    ProductAttributeValueListCreateView, ProductAttributeValueRetrieveUpdateDestroyView,
    ProductListView, ProductRetrieveUpdateDestroyView,
    ProductImageListCreateView, ProductImageRetrieveUpdateDestroyView,
    ProductCostListCreateView, ProductCostRetrieveUpdateDestroyView,
    ProductPriceListCreateView, ProductPriceRetrieveUpdateDestroyView, ProductCreateView, ManufacturerListCreateView,
    ManufacturerRetrieveUpdateDestroyView
)
app_name = 'catalog-api'
urlpatterns = [
    # Brand URLs
    path('brands/', BrandListCreateView.as_view(), name='brand-list-create'),
    path('brands/<int:pk>/', BrandRetrieveUpdateDestroyView.as_view(), name='brand-detail'),

    # Manufacturer URLs
    path('manufacturers/', ManufacturerListCreateView.as_view(), name='manufacturer-list-create'),
    path('manufacturers/<int:pk>/', ManufacturerRetrieveUpdateDestroyView.as_view(), name='manufacturer-detail'),


    # Product Attribute URLs
    path('attributes/', ProductAttributeListCreateView.as_view(), name='attribute-list-create'),
    path('attributes/<int:pk>/', ProductAttributeRetrieveUpdateDestroyView.as_view(), name='attribute-detail'),

    # Product Attribute Value URLs
    path('attribute-values/', ProductAttributeValueListCreateView.as_view(), name='attribute-value-list-create'),
    path('attribute-values/<int:pk>/', ProductAttributeValueRetrieveUpdateDestroyView.as_view(), name='attribute-value-detail'),

    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),


    # Product URLs
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),

    # Product Image URLs
    path('product-images/', ProductImageListCreateView.as_view(), name='product-image-list-create'),
    path('product-images/<int:pk>/', ProductImageRetrieveUpdateDestroyView.as_view(), name='product-image-detail'),

    # Product Cost URLs
    path('product-costs/', ProductCostListCreateView.as_view(), name='product-cost-list-create'),
    path('product-costs/<int:pk>/', ProductCostRetrieveUpdateDestroyView.as_view(), name='product-cost-detail'),

    # Product Price URLs
    path('product-prices/', ProductPriceListCreateView.as_view(), name='product-price-list-create'),
    path('product-prices/<int:pk>/', ProductPriceRetrieveUpdateDestroyView.as_view(), name='product-price-detail'),
]
