from rest_framework import serializers
# from account.models import Account
from .models import Addresses
from .models import Products
from .models import OrdersList
from .models import Orders
from account.models import Account


# class AccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = '__all__'

class AddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class OrdersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdersList
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['is_admin']
