'''
Models model for category app
'''
from django.db import models

# Create your models here.


class Category(models.Model):
    '''
    This class represents an ORM for The category database
    '''
    category_name = models.CharField(max_length=64, unique=True)
    category_description = models.CharField(max_length=255, blank=True)
    category_urlSlug = models.SlugField(max_length=128, unique=True)
    category_image = models.ImageField(
        upload_to='images/categories', blank=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        '''
        A string representation for the model
        '''
        return self.category_name
