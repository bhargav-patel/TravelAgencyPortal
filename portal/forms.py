from django import forms
from portal.models import Booking
from django.forms.extras.widgets import SelectDateWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from django.contrib.auth.models import User
from authentication.models import Profile
import datetime

class BookingForm(forms.ModelForm):
	booking_Date = forms.DateField(required=True,widget=SelectDateWidget(),initial=datetime.date.today)
	return_Date = forms.DateField(required=True,widget=SelectDateWidget(),initial=datetime.date.today)
	
	class Meta:
		model = Booking
		fields = ['booking_Date','return_Date','advance_Deposit']
		
	def __init__(self, *args, **kwargs):
		super(BookingForm, self).__init__(*args, **kwargs)
		self.fields['advance_Deposit'].required = True
		
	def clean(self):
		cleaned_data=super(BookingForm,self).clean()
		booking_Date = cleaned_data.get('booking_Date')
		return_Date = cleaned_data.get('return_Date')
		advance_Deposit = cleaned_data.get('advance_Deposit')
		if return_Date<=booking_Date:
			raise forms.ValidationError('Select Valid Dates.')
		if advance_Deposit<1000:
			raise forms.ValidationError('Deposit should be less than 1000.')

		return cleaned_data	

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name']
        
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile','address']

class ReturnForm(forms.Form):
    odometer_Reading = forms. IntegerField()