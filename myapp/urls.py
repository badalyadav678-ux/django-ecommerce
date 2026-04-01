from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),

    path('increase/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),

    path('payment/<int:order_id>/', views.payment, name='payment'),
    
    path('order-success/', views.order_success, name='order_success'),
    path('feedback/<int:order_id>/', views.feedback, name='feedback'),
    path('feedback-success/', views.feedback_success, name='feedback_success'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('add-to-wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]