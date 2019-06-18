from .models import Stock
from django.forms import ModelForm
from django import forms

class StockForm(ModelForm):
	class Meta:
		model = Stock
		fields = ('author', 'title')