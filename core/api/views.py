from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication, JWTAuthentication
from rest_framework import generics

from core.api.serializers import *

User = get_user_model()

# class Home(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)


class CountriesAPIView(generics.ListAPIView):
    serializer_class = CountriesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Country.objects.all()
        return queryset
    
class CitiesAPIView(generics.ListAPIView):
    serializer_class = CitiesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = City.objects.all()
        return queryset
    
class AddressesAPIView(generics.ListAPIView):
    serializer_class = AddressesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Address.objects.all()
        return queryset
    
class PhonesAPIView(generics.ListAPIView):
    serializer_class = PhonesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Phone.objects.all()
        return queryset
    
class CurrenciesAPIView(generics.ListAPIView):
    serializer_class = CurrenciesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Currency.objects.all()
        return queryset

class CurrencyRatesAPIView(generics.ListAPIView):
    serializer_class = CurrencyRatesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = CurrencyRate.objects.all()
        return queryset