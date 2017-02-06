from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import dbBoards
from .forms import SelectBoards, SearchBox, SearchResults, SearchSelected
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
			#test code that simply prints out a list of the names of the selected devices
			board_names = []
			for i in range(0, len((form.cleaned_data['boards']).only('name'))):
				print form.cleaned_data['boards'].only('name')[i]

			return HttpResponseRedirect('compare')
	return render(request, 'Home/home.html',{'form':form})

def search_boards(request):
	if 'search_input' not in request.session:
		request.session['search_input'] = ''
	print request.session['search_input']
	form_box = SearchBox()
	form_results = SearchResults()
	form_selected = SearchSelected()
	if request.method == 'POST':
		form_box = SearchBox(request.POST)
		form_box.fields['search_input'].attrs = {'class': 'form-control','id': 'searchInput','value': request.session['search_input']}
		if form_box.is_valid():
			request.session['search_input'] = request.POST.get('search_input', '') 
		form_results = SearchResults(request.POST)
		form_results.fields['search_output'].queryset = dbBoards.objects.filter(name__contains=request.session['search_input'])
		if form_results.is_valid():
			search_output = request.POST.get('search_output', '')

	# I somehow need to pass a variable from the input into the form, maybe a second form?
	return render(request, 'Home/search.html',{'form_box':form_box, 'form_results':form_results})

def compare(request):
	return render(request,'Home/compare.html')