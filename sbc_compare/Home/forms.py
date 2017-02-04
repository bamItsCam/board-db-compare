from django import forms
from .models import dbBoards
from django.core.exceptions import ValidationError

#Form for selecting boards on the Home page
class SelectBoards(forms.Form):
	boards = forms.ModelMultipleChoiceField(queryset=dbBoards.objects.only('name'), widget=forms.SelectMultiple(attrs={'class':'form-control','style': 'height: 120px;'}),label='')
	def clean(self):
		cleaned_data = super(SelectBoards, self).clean()
		if len(cleaned_data['boards']) > 5:
		    raise ValidationError("Too many boards selected! Try again.")
        	