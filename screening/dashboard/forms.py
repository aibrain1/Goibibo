from .models import Stock
from django.forms import ModelForm
from django import forms

#For ADD Values in Suggestion Search DropDown
class StockForm(ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Type Your Stock Name Here'}))
	class Meta:
		model = Stock
		fields = ('author', 'title')