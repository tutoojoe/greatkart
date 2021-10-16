from django.db import models
from django.urls import reverse
from django.urls.converters import SlugConverter

# Create your models here.
class Category(models.Model):
    category_name       = models.CharField(max_length=200, unique=True)
    slug                = models.SlugField(max_length=200, unique=True)
    description         = models.TextField(null=True, blank=True)
    category_image      = models.ImageField(upload_to ='photos/categories', null=True, blank=True)



    def __str__(self):
        return self.category_name

    def get_url(self):
        return reverse('products_by_category',args=[self.slug])


    
    class Meta:
        verbose_name        = 'Category'
        verbose_name_plural = 'Categories'

