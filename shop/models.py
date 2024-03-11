'''
Models model for product
'''
from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.


class Product(models.Model):
    '''
    This class represents The product database
    '''
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.category_urlSlug, self.slug])

    def __str__(self):
        return self.product_name


class VariationManager(models.Manager):
    """
    This class allows us to manage variations,
    and return the colors and sizes separately
    """

    def colors(self):
        """
        return only the colors varaitions
        """
        return super(VariationManager, self).filter(
            variation_category='color', is_active=True)

    def sizes(self):
        """
        return only the colors varaitions
        """
        return super(VariationManager, self).filter(
            variation_category='size', is_active=True)


variation_choices = (('color', 'color'),  # (stored value, readable value)
                     ('size', 'size'))


class Variation(models.Model):
    """
    This class represents the variation for each product 
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=128, choices=variation_choices)
    variation_value = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return f'{self.product.product_name}: {self.variation_value}'
