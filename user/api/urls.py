from django.urls import path
from .views import LogoutView
from user.api import views as api_views

app_name = 'user-api'

urlpatterns = [
    path('login/', api_views.CustomAuthToken.as_view()),
    path('logout/', LogoutView.as_view(), name ='logout'),
    path('email/check/',api_views.EmailValidityAPIView.as_view()),
    path('user/list/',api_views.UsersAPIView.as_view(), name ='users'),
    path('useraddress/list/',api_views.UserAddressesAPIView.as_view(), name ='useraddresses'),
    path('userphone/list/',api_views.UserPhonesAPIView.as_view(), name ='userphones'),
    path('userrole/list/',api_views.UserRolesAPIView.as_view(), name ='userroles'),
    path('userpermission/list/',api_views.UserPermissionsAPIView.as_view(), name ='userpermissions'),
    path('userresource/list/',api_views.UserResourcesAPIView.as_view(), name ='userresources'),
]