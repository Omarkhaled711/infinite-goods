'''
Models model for product
'''
from django.db import models
from category.models import Category
from django.urls import reverse
from django.db.models import Avg, Count
from users.models import User

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

    def avg_rating(self):
        """
        calculate the average rating of a product from reviews
        """
        avg = 0
        reviews = ReviewRating.objects.filter(
            product=self, status=True).aggregate(average=Avg('rating'))
        if (reviews and reviews['average'] is not None):
            avg = float(reviews['average'])
        return avg

    def count_reviewers(self):
        """
        count the number of users who reviewed the  product
        """
        count = 0
        reviews = ReviewRating.objects.filter(
            product=self, status=True).aggregate(count=Count('id'))
        if (reviews and reviews['count'] is not None):
            count = int(reviews['count'])
        return count


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


class ReviewRating(models.Model):
    """
    This class represents the review and ratings table
    in the database
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=128, blank=True)
    review = models.CharField(max_length=512, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=28, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} on {self.product}: {self.subject}'
