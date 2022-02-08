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
        fields = ['id', 'recipient_name', 'address']

class AddressesDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = ['id', 'is_active']


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        exclude = ['is_active']


class ProductsDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['prod_id','is_active']


class OrdersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdersList
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class OrdersESerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['id', 'addresses_id']


class OrdersSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['order_status','batch_id']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['is_admin']
