from django import forms
from django.db.models import fields
from .models import ReviewRating, Product,ProductGallery


class Reviewforms(forms.ModelForm):

    class Meta:
        model = ReviewRating
        fields = ['subject','review','rating']


# class ProductGalleryForms(forms.Modelform):
#     image = forms.ImageField(required=False, error_messages={'invalid':"Image Files Only"}, widget=forms.FileInput)
#     class Meta:
#         model = ProductGallery
#         fields = ['product','image']



class ProductForm(forms.ModelForm):
    images = forms.ImageField(required=False, error_messages={'invalid':"Image Files Only"}, widget=forms.FileInput)
    class Meta:
        model = Product
        fields = ('product_name', 'description', 'price','images','stock','is_available','category')

    def __init__(self,*args,**kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        
   
        

