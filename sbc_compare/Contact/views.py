from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template
from .forms import ContactForm


# Create your views here.

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
			template = get_template('Contact/contact_template.html')
			context = Context({'contact_name': contact_name,'contact_email': contact_email,'form_content': form_content,})
			content = template.render(context)

			email = EmailMessage("New contact form submission",content,contact_name + '',['sbccompare@gmail.com'],headers = {'Reply-To': contact_email })
			email.send()
			return redirect('contact')


	return render(request,'Contact/contact.html',{'form':form_class})