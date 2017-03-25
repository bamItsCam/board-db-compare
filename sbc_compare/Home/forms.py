from django import forms
from .models import dbBoards
from django.core.exceptions import ValidationError

#Form for selecting boards on the Home page
class SelectBoards(forms.Form):
	boards = forms.ModelMultipleChoiceField(queryset=dbBoards.objects.only('name'), 
											widget=forms.SelectMultiple(attrs={'class':'form-control','style': 'height: 120px;'}),
											label='')
	
	#ef clean(self):
	#	cleaned_data = super(SelectBoards, self).clean()
	#	if len(cleaned_data['boards']) > 5:
	#	    raise ValidationError("Too many boards selected! Try again.")
        	

class SearchBox(forms.Form):
	search_input = forms.CharField(
    	required=False,
    	widget=forms.TextInput(attrs={'class':'form-control', 'id': 'search_form'}),
    	label="Name"
    	)

	#def clean(self):
	#	cleaned_data = super(SearchBox, self).clean()

class SearchResults(forms.Form):
	search_output = forms.ModelChoiceField(queryset=dbBoards.objects.all(), 
											widget=forms.SelectMultiple(attrs={'class':'form-control','style': 'height: 240px;'}),
											label='',
											required=False)

	def clean(self):
		if 'add' in self.data:
			cleaned_data = super(SearchResults, self).clean()

class SearchSelected(forms.Form):
	selected_boards = forms.ModelChoiceField(queryset=dbBoards.objects.none(), 
											widget=forms.SelectMultiple(attrs={'class':'form-control','style': 'height: 240px;'}),
											label='',
											required=False)

	def clean(self):
		cleaned_data = super(SearchSelected, self).clean()