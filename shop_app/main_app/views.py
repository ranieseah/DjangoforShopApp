from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Products
from .serializers import ProductsSerializer
from account.models import Account, AccountManager
from .serializers import AccountSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import AdminSerializer


def hello(request):
    return HttpResponse('checking if server is liveeee')


class AddProduct(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):
        add = Products.objects.create(prod_id=request.data['prod_id'], price=request.data['price'], description=request.data['description'], qty=request.data['qty'], image=request.data['image'])
        add.save()
        # show = Products.objects.all()
        # serializer = ProductsSerializer(show, many =True)
        # return Response(serializer.data)
        return JsonResponse({"msg": "OK"})


class ViewProducts(APIView):
    def get(self, request):
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many = True)
        return Response(serializer.data)


class UpdateProduct(APIView):
    permission_classes = (IsAdminUser,)
    def put(self, request):
        print(request.data['prod_id'])
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
            check_admin = Account.objects.get(email=request.data['email'])
            serializer = AdminSerializer(check_admin, many=False)
            print(serializer.data)
            return Response(serializer.data)
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

