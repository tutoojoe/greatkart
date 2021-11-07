from django import forms
from django.db.models import fields
from .models import Category






class CategoryForm(forms.ModelForm):
    category_image = forms.ImageField(required=False, error_messages={'invalid':"Image Files Only"}, widget=forms.FileInput)
    class Meta:
        model = Category
        fields = ('category_name', 'description', 'category_image')

    def __init__(self,*args,**kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'