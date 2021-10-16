from enum import unique
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DecimalField
import category
from django.urls import reverse
from category.models import Category

# Create your models here.

class Product(models.Model):
    product_name        = models.CharField(max_length=200,unique=True)
    slug                = models.SlugField(max_length=200,unique=True)
    description         = models.TextField(null=True,blank=True)
    price               = models.DecimalField(max_digits=10, decimal_places=2)
    images              = models.ImageField(upload_to='photos/products',null=True, blank=True)
    stock               = models.IntegerField()
    is_available        = models.BooleanField(default=True)
    category            = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date        = models.DateTimeField(auto_now_add=True)
    modiified_date      = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])

    def __str__(self):
        return self.product_name

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category = 'color', is_active = True)
    def sizes(self):
        return super(VariationManager,self).filter(variation_category = 'size', is_active = True)
               
variation_category_choice = (
    ('color','color'),
    ('size','size'),
)
class Variation(models.Model):
    product             = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category  = models.CharField(max_length=100,choices=variation_category_choice)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now_add=True)

    objects             = VariationManager()

    def __str__(self):
        return self.variation_value