from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu', views.menu, name="menu"),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('item/<str:thing>/<int:id>', views.item, name='item'),
    path('cart', views.cart, name='cart'),
    path('orders', views.orders, name="orders"),
    path('order/<int:order_id>', views.order, name="order"),
    path('account', views.my_account, name="my_account"),
    path('placed', views.placed, name="placed"),
    path('address/<int:id>', views.address, name="address"),
]