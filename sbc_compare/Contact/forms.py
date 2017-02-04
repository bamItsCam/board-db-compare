from django import forms
from django.core.exceptions import ValidationError

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