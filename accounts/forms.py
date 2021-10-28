from django import forms
from django.db import models
from django.db.models import fields
from .models import Account,Address, UserProfile


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
    


class AddAddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['first_name','last_name','mobile','email','address_line_1','address_line_2','city','district','state','country','pincode']
       



    def __init__(self,*args,**kwargs):
        super(AddAddressForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter Firstname'
        self.fields['last_name'].widget.attrs['placeholder']='Enter last name'
        self.fields['mobile'].widget.attrs['placeholder']='Enter Mobile number'
        self.fields['email'].widget.attrs['placeholder']='Enter email address'
        self.fields['address_line_1'].widget.attrs['placeholder']='Enter your address'
        self.fields['address_line_2'].widget.attrs['placeholder']='Enter your address'
        self.fields['city'].widget.attrs['placeholder']='Enter City Name'
        self.fields['district'].widget.attrs['placeholder']='Enter your district'
        self.fields['state'].widget.attrs['placeholder']='Enter State'
        self.fields['country'].widget.attrs['placeholder']='Enter Country'
        self.fields['pincode'].widget.attrs['placeholder']='Enter Pincode'

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


class Userform(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'mobile_number')

    def __init__(self,*args,**kwargs):
        super(Userform, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'




class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'invalid':"Image Files Only"}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1','address_line_2','city','state','country','profile_picture')

    def __init__(self,*args,**kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'