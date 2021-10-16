from django import forms
from django.db import models
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Confirm Password'
    }))

    class Meta:
        model = Account
        fields = ['first_name','last_name','email','mobile_number','password']
        # will generate the username from the email id input

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords doesn't match.")

    def __init__(self,*args,**kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter Firstname'
        self.fields['last_name'].widget.attrs['placeholder']='Enter Lastname'
        self.fields['email'].widget.attrs['placeholder']='Enter valid Email'
        self.fields['mobile_number'].widget.attrs['placeholder']='Enter Mobile Number'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
    
