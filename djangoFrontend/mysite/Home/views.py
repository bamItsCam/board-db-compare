from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import dbBoards
from .forms import SelectBoards
from django.core.management import call_command

#call_command('populate_db') This currently takes a lot of time...I think it should only be run once a week or something

def contact(request):
	return render(request,'Home/contact.html')

def about(request):
	return render(request,'Home/about.html')

#Displays the SelectBoards form and allows the user to select boards. 
#TODO: use input data from form to query Attribute database and return the attribute sets for the selected boards
def select_boards(request):
	form = SelectBoards()
	if request.method == "POST":
		form = SelectBoards(request.POST)
		if form.is_valid():
			board_names = []
			for i in range(0, len((form.cleaned_data['boards']).values_list('name'))):
				board_names.append((form.cleaned_data['boards']).values_list('name')[i])
			for j in range(0, len(board_names)):
				#LOL...this line
				board_names[j] = ((str(board_names[j]).strip('u(')).strip(',)')).strip("'")
			#print board_names
			return HttpResponseRedirect('/compare/')
	return render(request, 'Home/home.html',{'form':form})

def compare(request):
	return render(request,'Home/compare.html')