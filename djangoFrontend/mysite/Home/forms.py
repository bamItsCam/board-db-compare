from django import forms
from .models import dbBoards

#Form for selecting boards on the Home page
class SelectBoards(forms.Form):
	boards = forms.ModelMultipleChoiceField(queryset=dbBoards.objects.all(), widget=forms.SelectMultiple(attrs={'class':'form-control'}),label='')