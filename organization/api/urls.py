from django.urls import path
from .views import *
from organization.api import views as api_views

app_name = 'organization-api'

urlpatterns = [
    path('organization/list/', OrganizationsAPIView.as_view(), name ='organizations'),
    path('organizationuser/list/', OrganizationUsersAPIView.as_view(), name ='organizationusers'),
    path('position/list/', PositionsAPIView.as_view(), name ='positions'),
    path('department/list/', DepartmentsAPIView.as_view(), name ='departments'),
]