'''
Module for orders urls
'''
from django.urls import include, path
from orders import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_completed/', views.order_completed, name='order_completed'),
    path('api/v1/', include('orders.api.v1.urls')),
]
