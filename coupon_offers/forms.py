from django import forms
from django.db.models import fields
from .models import Coupon,ProductOffer,CategoryOffer


class CouponApplyForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code','valid_from','valid_to','discount','active']
    
        def __init__(self,*args,**kwargs):
            super(CouponApplyForm, self).__init__(*args, **kwargs)
        

    # code = forms.CharField()

class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = ['code','product_id', 'valid_from','valid_to','discount','is_active']
    
        def __init__(self,*args,**kwargs):
            super(ProductOfferForm, self).__init__(*args, **kwargs)

class CategoryOfferForm(forms.ModelForm):
    class Meta:
        model = CategoryOffer
        fields = ['code','category_id', 'valid_from','valid_to','discount','is_active']
    
        def __init__(self,*args,**kwargs):
            super(CategoryOfferForm, self).__init__(*args, **kwargs)
            