'''
Admin model for the category app
'''
from django.contrib import admin
from category.models import Category
# Register your models here.


class ManageCategory(admin.ModelAdmin):
    '''
    Make slug pre populated based on category name
    and edit what is being displayed
    '''
    prepopulated_fields = {'category_urlSlug': ('category_name',)}
    list_display = ('category_name', 'category_urlSlug')


admin.site.register(Category, ManageCategory)
