from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.deletion import SET_NULL
from django.utils.translation import activate

from store.models import Product,Category


# Create your models here.


class Coupon(models.Model):
    code        = models.CharField(max_length=50,unique=True,)
    valid_from  = models.DateTimeField()
    valid_to    = models.DateTimeField()
    discount    = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(75)])
    active      = models.BooleanField()

    

    def __str__(self):
        return self.code

    


class ProductOffer(models.Model):
    product_id      = models.ForeignKey(Product,on_delete=SET_NULL,null=True, blank=True)
    code            = models.CharField(max_length=50, unique=True)
    valid_from      = models.DateTimeField()
    valid_to        = models.DateTimeField()
    discount        = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(75)])
    is_active       = models.BooleanField()

    def __str__(self):
        return self.code
    
    def disc_product_price(self):
        original_price = self.product_id.price
        disc_price = original_price - (original_price*(self.discount/100))
        return disc_price
   

class CategoryOffer(models.Model):
    category_id     = models.ForeignKey(Category,on_delete=SET_NULL,null=True, blank=True)
    code            = models.CharField(max_length=50, unique=True)
    valid_from      = models.DateTimeField()
    valid_to        = models.DateTimeField()
    discount        = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(75)])
    is_active       = models.BooleanField()

    def __str__(self):
        return self.code
    
    def disc_product_price(self):
        original_price = self.category_id.product.price
        disc_price = original_price - (original_price*(self.discount/100))
        return disc_price