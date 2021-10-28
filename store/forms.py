from django import forms
from django.db.models import fields
from .models import ReviewRating


class Reviewforms(forms.ModelForm):

    class Meta:
        model = ReviewRating
        fields = ['subject','review','rating']
        

