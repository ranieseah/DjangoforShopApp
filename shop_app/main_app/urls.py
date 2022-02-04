from django.urls import path
from . import views
from rest_framework_simplejwt.views import(TokenRefreshView)

urlpatterns=[
    path('hello/', views.hello),
    path('products/', views.ViewProducts.as_view()),
    path('add-product/', views.AddProduct.as_view()),
    path('update-product/', views.UpdateProduct.as_view()),
    path('del-product/', views.DelProduct.as_view()),
    path('user/', views.ViewUser.as_view()),
    path('login/', views.AuthUser.as_view()),
    path('user-token/', views.UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin-token/', views.AdminTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('add-user/', views.AddUser.as_view()),
    path('add-super-user/', views.AddSUser.as_view()),

]
