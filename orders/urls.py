from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('item/<str:thing>/<int:id>', views.item, name='item'),
    path('cart', views.cart, name='cart'),
    path('orders', views.orders, name="orders")
]