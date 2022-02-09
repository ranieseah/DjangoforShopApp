from django.urls import path
from . import views
from rest_framework_simplejwt.views import(TokenRefreshView)

urlpatterns=[
    path('hello/', views.hello),
    path('products/', views.ViewProducts.as_view()),
    path('add-product/', views.AddProduct.as_view()),
    path('product-details/', views.ProductDetail.as_view()),
    path('update-product/', views.UpdateProduct.as_view()),
    path('del-product/', views.DelProduct.as_view()),
    path('remove-product/',views.RemoveProduct.as_view()),
    path('user/', views.ViewUser.as_view()),
    path('login/', views.AuthUser.as_view()),
    path('user-token/', views.UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin-token/', views.AdminTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('add-user/', views.AddUser.as_view()),
    path('add-super-user/', views.AddSUser.as_view()),
    path('add-address/', views.AddAddress.as_view()),
    path('address/', views.ViewAddress.as_view()),
    path('update-address/', views.UpdateAddress.as_view()),
    path('del-address/', views.DelAddress.as_view()),
    path('add-orders/', views.AddOrders.as_view()),
    path('view-own-orders-list/', views.ViewOwnOrdersList.as_view()),
    path('view-orders/', views.ViewOrders.as_view()),
    path('view-prod-stats/', views.ViewProdStats.as_view()),
    path('del-orders/', views.DelOrders.as_view()),
    path('edit-orders/', views.EditOrders.as_view()),
    path('edit-status/', views.EditStatus.as_view()),

]
