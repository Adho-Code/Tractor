from django import forms
from bootstrap_datepicker_plus import *
from .models import *

class TractorForm(forms.ModelForm):
    class Meta:
        model = Tractor
        exclude = ['user']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['username','tractor_id']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['prof_user','all_tractors']

# class BookingForm(forms.Form):
#     your_name = forms.CharField(label='Enter Username',max_length=100)
#     email = forms.EmailField(label='Email')
#     location = forms.CharField(label='Current Location',max_length=100)
#     booked_date = forms.DateField()
