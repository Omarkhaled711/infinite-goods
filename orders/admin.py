"""
Registem orders app models to the admin page
"""
from django.contrib import admin
from orders.models import Order, OrderProduct, Payment
# Register your models here.


class OrderProductsInline(admin.TabularInline):
    """
    Show the order products of each order, under the order's table
    """
    model = OrderProduct
    extra = 0
    readonly_fields = ['payment', 'user', 'product',
                       'quantity', 'ordered', 'product_price']


class OrderAdmin(admin.ModelAdmin):
    """
    Customize the appearance of the order's model on the admin page
    """
    list_display = ['order_id', 'full_name', 'email', 'phone',
                    'full_address', 'total', 'tax', 'discount', 'status', 'is_ordered']
    list_filter = ['is_ordered', 'status']
    search_fields = ['order_id', 'first_name', 'last_name', 'email', 'phone']
    list_per_page = 20
    inlines = [OrderProductsInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Payment)
