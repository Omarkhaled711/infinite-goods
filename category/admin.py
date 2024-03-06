'''
Admin model for the category app
'''
from django.contrib import admin
from category.models import Category
# Register your models here.

admin.site.register(Category)
