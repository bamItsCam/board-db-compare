from django import forms
from .models import dbBoards

#Form for selecting boards on the Home page
class SelectBoards(forms.Form):
	boards = forms.ModelMultipleChoiceField(queryset=dbBoards.objects.only('name'), widget=forms.SelectMultiple(attrs={'class':'form-control','style': 'height: 120px;'}),label='')

#Form for sending emails to the developers :) I have an interest in learning how to set up an email server for a site. Right now the messages are just being
#sent to the console (where the manage commands are run for the dev server) but eventually I want there to be an actual email account for this site :D
class ContactForm(forms.Form):
    contact_name = forms.CharField(
    	required=True,
    	widget=forms.TextInput(attrs={'class':'form-control'}),
    	label="Name"
    	)
    contact_email = forms.CharField(
    	required=True,
    	widget=forms.EmailInput(attrs={'class':'form-control'}),
    	label='Email Address'
    )
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class':'form-control'}),
        label='Message'
    )