from django.contrib import admin
from .models import Product, Order, OrderItem, Feedback
from .models import Wishlist



class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'status', 'created_at']


admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Feedback)
admin.site.register(Wishlist)