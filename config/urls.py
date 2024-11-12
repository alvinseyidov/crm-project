from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include
from django.urls.conf import re_path
from django.conf.urls.static import static
from django.conf import settings

from core import views as core_views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="ERP API",
      default_version='v1',
      description="ERP APP swagger",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.index, name='index'),
    path("__debug__/", include("debug_toolbar.urls")),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += [
    path('api/user/',include('user.api.urls',namespace='user-api')),
    path('api/core/',include('core.api.urls',namespace='core-api')),
    path('api/inventory/',include('inventory.api.urls',namespace='inventory-api')),
    path('api/accounting/',include('accounting.api.urls',namespace='accounting-api')),
    path('api/purchase/',include('purchase.api.urls',namespace='purchase-api')),
    path('api/organization/',include('organization.api.urls',namespace='organization-api')),
    path('api/catalog/',include('catalog.api.urls',namespace='catalog-api')),
    path('api/user-auth/',include('auth.api.urls',namespace='user-auth-api')),
    path('api/sale/',include('sale.api.urls',namespace='sale-api')),
    path('api/expense/',include('expense.api.urls',namespace='expense-api')),
    path('api/hr/',include('hr.api.urls',namespace='hr-api')),
    path('api/customer/',include('customer.api.urls',namespace='customer-api')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



