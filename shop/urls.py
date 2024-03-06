from django.urls import path
from . import views

urlpatterns = [
    path ('', views.shop, name='shop'),
    path ('<slug:category_slug>/', views.shop, name='products_category'),
]