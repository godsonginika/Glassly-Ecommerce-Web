from django.urls import path
from store import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('shop/<int:pk>', views.product_detail, name='product_detail'),
]