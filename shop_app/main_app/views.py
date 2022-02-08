import jwt,json
import uuid
from django.db.models import Q
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Products, Addresses, OrdersList, Orders
from .serializers import ProductsSerializer, AddressesSerializer, AddressesDSerializer, ProductsDSerializer, \
    OrdersListSerializer, OrdersSerializer, OrdersESerializer, OrdersSSerializer
from account.models import Account, AccountManager
from .serializers import AccountSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import AdminSerializer
from shop_app.settings import SECRET_KEY

def hello(request):
    return HttpResponse('checking if server is liveeee')


class AddProduct(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        add = Products.objects.create(prod_id=request.data['prod_id'],name=request.data['name'], price=request.data['price'], description=request.data['description'], qty=request.data['qty'], image=request.data['image'])
        add.save()
        # show = Products.objects.all()
        # serializer = ProductsSerializer(show, many =True)
        # return Response(serializer.data)
        return JsonResponse({"msg": "OK"})


class ViewProducts(APIView):
    def get(self, request):
        products = Products.objects.filter(is_active=True)
        serializer = ProductsSerializer(products, many = True)
        return Response(serializer.data)


class UpdateProduct(APIView):
    permission_classes = (IsAdminUser,)

    def put(self, request):
        product = Products.objects.get(prod_id=request.data['prod_id'])
        serializer = ProductsSerializer(instance=product, data = request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"msg": "OK"})
        else:
            return JsonResponse({"msg": "Error: Unable to save to Table."})

class DelProduct(APIView):
    permission_classes = (IsAdminUser,)

    def delete(self, request):
        product = Products.objects.get(prod_id=request.data['prod_id'])
        serializer = ProductsDSerializer(instance=product, data = request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"msg": "OK"})
        else:
            return JsonResponse({"msg": "Error: Unable to save to Table."})

class RemoveProduct(APIView):
    permission_classes = (IsAdminUser,)

    def delete(self, request):
        product = Products.objects.get(prod_id=request.data['prod_id'])
        product.delete()
        return JsonResponse({"msg": "OK"})

class AddUser(APIView):
    def post(self, request):
        Account.objects.create_user(email=request.data['email'], name=request.data['name'], surname=request.data['surname'], password=request.data['password'])
        return JsonResponse({"msg": "OK"})

class AddSUser(APIView):
    def post(self, request):
        Account.objects.create_superuser(email=request.data['email'], name=request.data['name'], surname=request.data['surname'], password=request.data['password'])
        return JsonResponse({"msg": "OK"})

# class ViewUser(APIView):
#     def get(self, request):
#         users = Account.objects.get(email=request.data['email'])
#         serializer = AccountSerializer(users, many=False)
#         return Response(serializer.data)

class AuthUser(APIView):
    def post(self, request):
        user = authenticate(email=request.data['email'], password=request.data['password'])
        if user is not None:
            # check_admin = Account.objects.get(email=request.data['email'])
            # serializer = AdminSerializer(check_admin, many=False)
            # print(serializer.data)
            # return Response(serializer.data)

            # user_info = Account.objects.get(email=request.data['email'])
            # serializer = AccountSerializer(user_info, many=False)
            # payload = {
            #     'email': request.data['email'],
            #     'id': serializer.data['id'],
            #     'is_admin': serializer.data['is_admin'],
            #     'name' : serializer.data['name']
            # }
            # jwt_token = {'token': jwt.encode(payload, SECRET_KEY)}
            #
            # return HttpResponse(json.dumps(jwt_token),status=200,content_type="application/json")

            return JsonResponse({"msg":"OK"})
        else:
            # Return an 'invalid login' error message.
            return JsonResponse({"msg":"Error - user not logged"})

class UserTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls,user):
        token=super().get_token(user)
        token['admin'] = 'false'

        return token

class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls,user):
        token=super().get_token(user)

        token['admin'] = 'true'
        return token

class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer

class AddAddress(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        add = Addresses.objects.create(recipient_name=request.data['recipient_name'], address=request.data['address'], account_of_id=request.data['account_of_id'])
        add.save()
        return JsonResponse({"msg": "OK"})

class ViewAddress(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        header = request.headers.get('Authorization')
        token = header[7:]
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
        user = payload['user_id']
        user_add= Addresses.objects.filter(account_of_id=user,is_active=True)
        serializer = AddressesSerializer(user_add, many = True)
        return Response(serializer.data)

class UpdateAddress(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        address = Addresses.objects.get(id=request.data['id'])
        serializer = AddressesSerializer(instance=address, data = request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"msg": "OK"})
        else:
            return JsonResponse({"msg": "Error: Unable to save to Table."})

class DelAddress(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        address = Addresses.objects.get(id=request.data['id'])
        serializer = AddressesDSerializer(instance=address, data = request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"msg": "OK"})
        else:
            return JsonResponse({"msg": "Error: Unable to save to Table."})
        # delete = Addresses.objects.get(id=request.data['id'])
        # delete.delete()
        # return JsonResponse({"msg": "OK"})

class AddOrders(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        for order in request.data:
            for product in order['prod_id']:
                minus = Products.objects.get(prod_id=product)
                if minus.qty == 0:
                    return JsonResponse({"msg": "sorry, we've run out of some stocks."})
                else:
                    minus.qty -= 1
                    minus.save()
        # problem - no roll back if there's insufficient stocks halfway thru the submission.
        header = request.headers.get('Authorization')
        token = header[7:]
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
        user = payload['user_id']
        add = OrdersList.objects.create(account_of_id=user)
        add.save()
        string = str(add)
        batch_id = uuid.UUID(string)
        for order in request.data:
            for product in order['prod_id']:
                add_order = Orders.objects.create(batch_id_id=batch_id, addresses_id_id=order['addresses_id'])
                add_order.save()
                new_order = str(add_order)
                this_order = Orders.objects.get(id=new_order)
                this_order.prod_id.add(product)

        return JsonResponse({"msg": "OK"})

class ViewOwnOrdersList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        header = request.headers.get('Authorization')
        token = header[7:]
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
        user = payload['user_id']

        order_list = OrdersList.objects.filter(account_of=user)
        serializer = OrdersListSerializer(order_list, many = True)

        return Response(serializer.data)

class ViewOrders(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        orders = Orders.objects.filter(batch_id_id=request.data['batch_id'])
        serializer = OrdersSerializer(orders, many = True)
        return Response(serializer.data)

class ViewProdStats(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        PRorders = Orders.objects.filter(prod_id=request.data['prod_id'], order_status="PR").aggregate(count=Count('id'))
        RYorders = Orders.objects.filter(prod_id=request.data['prod_id'], order_status="RY").aggregate(count=Count('id'))
        DEorders = Orders.objects.filter(prod_id=request.data['prod_id'], order_status="DE").aggregate(count=Count('id'))
        CMorders = Orders.objects.filter(prod_id=request.data['prod_id'], order_status="CM").aggregate(count=Count('id'))
        return JsonResponse({"Processing": PRorders['count'], "Ready":RYorders['count'], "Out for Delivery":DEorders['count'], "Completed":CMorders['count']})

class DelOrders(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):

        order = Orders.objects.get(id=request.data['id'])
        serializer = OrdersSerializer(order, many=False)
        plus = Products.objects.get(prod_id=serializer.data['prod_id'][0])
        plus.qty += 1
        plus.save()
        last_order = Orders.objects.filter(batch_id=serializer.data['batch_id'])
        is_lastorder = OrdersSerializer(last_order, many=True)
        if len(is_lastorder.data) == 1:
            order.delete()
            batch = OrdersList.objects.get(batch_id=serializer.data['batch_id'])
            batch.delete()
        else:
            order.delete()

        return JsonResponse({"msg": "OK"})

class EditOrders(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):

        edit = Orders.objects.get(id=request.data['id'])
        serializer = OrdersSerializer(edit, many=False)
        edit_serializer = OrdersESerializer(instance=edit, data=request.data, partial=False)
        plus = Products.objects.get(prod_id=serializer.data['prod_id'][0])
        plus.qty += 1
        plus.save()
        minus = Products.objects.get(prod_id=request.data['prod_id'])
        minus.qty -= 1
        minus.save()
        edit.prod_id.clear()
        edit.prod_id.add(request.data['prod_id'])

        if edit_serializer.is_valid():
            edit_serializer.save()
            return JsonResponse({"msg": "OK"})
        else:
            return JsonResponse({"msg": "Error: Unable to save to Table."})


class EditStatus(APIView):
    permission_classes = (IsAdminUser,)

    def put(self, request):

        edit = Orders.objects.get(id=request.data['id'])
        serializer = OrdersSSerializer(edit, many=False)
        if serializer.data['order_status'] == 'PR':
            edit.order_status = 'RY'
            last_order = Orders.objects.filter(batch_id=serializer.data['batch_id'], order_status='PR')
            is_lastorder = OrdersSSerializer(last_order, many=True)
            if len(is_lastorder.data) == 1:
                batch = OrdersList.objects.get(batch_id=serializer.data['batch_id'])
                batch.order_status = 'RY'
                batch.save()
        elif serializer.data['order_status'] == 'RY':
            edit.order_status = 'DE'
            last_order = Orders.objects.filter(Q(batch_id=serializer.data['batch_id']), Q(order_status='PR') | Q(order_status='RY'))
            is_lastorder = OrdersSSerializer(last_order, many=True)
            if len(is_lastorder.data) == 1:
                batch = OrdersList.objects.get(batch_id=serializer.data['batch_id'])
                batch.order_status = 'DE'
                batch.save()
        else:
            edit.order_status = 'CM'
            last_order = Orders.objects.filter(Q(batch_id=serializer.data['batch_id']), Q(order_status='PR') | Q(order_status='RY') | Q(order_status='DE'))
            is_lastorder = OrdersSSerializer(last_order, many=True)
            if len(is_lastorder.data) == 1:
                batch = OrdersList.objects.get(batch_id=serializer.data['batch_id'])
                batch.order_status = 'CM'
                batch.save()
        edit.save()

        return JsonResponse({"msg": "OK"})
