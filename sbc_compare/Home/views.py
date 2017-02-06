from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import dbBoards
from .forms import SelectBoards
from django.core.management import call_command

#call_command('populate_db') This currently takes a lot of time...I think it should only be run once a week or something

def about(request):
	return render(request,'Home/about.html')

#Displays the SelectBoards form and allows the user to select boards. 
#TODO: Add code for fetching and processing attribute sets, figure out how to send the attribute sets to the compare page
def select_boards(request):
	form = SelectBoards()
	if request.method == "POST":
		form = SelectBoards(request.POST)
		if form.is_valid():
			form_list = []
			#form_dict = {}
			form_data = form.cleaned_data['boards'].values()
			for item in form_data:
   				#name = item['name']
   				#form_dict[name] = item
   				form_list.append(dict(item))
   			print form_list
			#return HttpResponseRedirect('/compare/')
			return render(request, 'Home/compare.html', {'selected': form_list})
	return render(request, 'Home/home.html',{'form':form})

def compare(request):
	return render(request,'Home/compare.html')