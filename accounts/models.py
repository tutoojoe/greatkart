from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.deletion import CASCADE
from django.db.models.fields import EmailField
from django.db.models.fields.related import OneToOneField

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,mobile_number,password=None):
        if not email:
            raise ValueError('User must provide a valid email.')
        
        if not username:
            raise ValueError('Provide a unique username.')
        
        if not mobile_number:
            raise ValueError('Prvode a valid mobile number')
        
        else:
            user = self.model(
                email       = self.normalize_email(email),
                username    = username,
                first_name  = first_name,
                last_name   = last_name,
                mobile_number= mobile_number    
            )
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self,first_name,last_name,email,username,mobile_number,password):
        user = self.create_user(
            email           = self.normalize_email(email),
            username        = username,
            password        = password,
            first_name      = first_name,
            last_name       = last_name,
            mobile_number   = mobile_number
            )
        user.is_admin       = True
        user.is_staff       = True
        user.is_active      = True
        user.is_superuser   = True
        
        user.save(using=self._db)
        return user





class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique = True)
    email           = models.EmailField(max_length=100, unique = True)
    mobile_number    = models.CharField(max_length=50)

    #required fields
    date_joined     = models.DateTimeField(auto_now_add = True)
    last_login      = models.DateTimeField(auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)

    # setting 'email' as the default login parameter
    USERNAME_FIELD  = 'email'
    # setting up the mandatory fields for registration form
    REQUIRED_FIELDS = ['username','first_name','last_name','mobile_number']

    # adding a User Manager to control users - BaseUserManager
    objects = MyAccountManager()

    # Function to show the desired value to be displayed on the table/while printing. 
    # Eg: firstname
    def __str__(self):
        return self.first_name + ' | ' + self.email
    
    def  full_name(self):
        return f'{self.first_name} {self.last_name}'


    # Setting up permissions to user
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True


class Otp(models.Model):
    otp     = models.IntegerField(null=True,blank=True)
    user    = models.CharField(max_length=100)

    def __unicode__(self):
        return self.user



class Address(models.Model):

    user            = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    mobile          = models.CharField(max_length=15, blank=True, null=True)
    email           = models.EmailField(max_length=50, blank=True, null=True)    
    address_line_1  = models.CharField(max_length=100,  blank=True, null=True)
    address_line_2  = models.CharField(max_length=100, blank=True)
    city            = models.CharField(max_length=50)
    district        = models.CharField(max_length=50)
    state           = models.CharField(max_length=50)
    country         = models.CharField(max_length=50, blank=True, null=True)
    pincode         = models.CharField(max_length=10,blank=True, null=True) 

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    
    def  full_name(self):
        return f'{self.first_name} {self.last_name}'
        
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'



class UserProfile(models.Model):
    user            = models.OneToOneField(Account, on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank = True,upload_to = 'userprofile')
    address_line_1  = models.CharField(max_length = 100, blank=True, null=True)
    address_line_2  = models.CharField(max_length = 100, blank=True, null=True)
    city            = models.CharField(max_length = 20, blank=True, null=True)
    state           = models.CharField(max_length = 20, blank=True, null=True)
    country         = models.CharField(max_length = 20, blank=True, null=True)

    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    


    