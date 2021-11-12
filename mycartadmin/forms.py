from django import forms
from django.forms import widgets

from .models import BannerUpdate

class DateInput(forms.DateTimeInput):
    input_type = 'date'

class BannerUpdateForm(forms.ModelForm):
    class Meta:
        model = BannerUpdate
        fields = ['banner_image','banner_name','valid_from','valid_to','is_active']
        widgets = {
            'valid_from': DateInput(),
            'valid_to':DateInput(),
        }


        def __init__(self,*args,**kwargs):
                super(BannerUpdateForm, self).__init__(*args, **kwargs)