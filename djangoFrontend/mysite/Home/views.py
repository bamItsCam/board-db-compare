from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import dbBoards
from .forms import SelectBoards, ContactForm
from django.core.management import call_command
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template

#call_command('populate_db') This currently takes a lot of time...I think it should only be run once a week or something

#Handles the contact form on the Contact page
def contact(request):
	form_class = ContactForm
	if request.method == 'POST':
		form = form_class(data=request.POST)

		if form.is_valid():
			contact_name = request.POST.get('contact_name', '')
			contact_email = request.POST.get('contact_email', '')
			form_content = request.POST.get('content', '')
            # Email the profile with the 
            # contact information
			template = get_template('Home/contact_template.html')
			context = Context({'contact_name': contact_name,'contact_email': contact_email,'form_content': form_content,})
			content = template.render(context)

			email = EmailMessage("New contact form submission",content,"Your website" +'',['youremail@gmail.com'],headers = {'Reply-To': contact_email })
			email.send()
			return redirect('contact')


	return render(request,'Home/contact.html',{'form':form_class})

def about(request):
	return render(request,'Home/about.html')

#Displays the SelectBoards form and allows the user to select boards. 
#TODO: Add code for fetching and processing attribute sets, figure out how to send the attribute sets to the compare page
def select_boards(request):
	form = SelectBoards()
	if request.method == "POST":
		form = SelectBoards(request.POST)
		if form.is_valid():
			#test code that simply prints out a list of the names of the selected devices
			board_names = []
			for i in range(0, len((form.cleaned_data['boards']).only('name'))):
				print form.cleaned_data['boards'].only('name')[i]

			return HttpResponseRedirect('/compare/')
	return render(request, 'Home/home.html',{'form':form})

def compare(request):
	return render(request,'Home/compare.html')