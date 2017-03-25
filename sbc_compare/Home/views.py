from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string

from .models import dbBoards
from .forms import SelectBoards, SearchBox, SearchResults, SearchSelected
from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt

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
@csrf_exempt
def search_boards(request):
	form_search = SearchBox()
	form_results = SearchResults()
	form_selected = SearchSelected()

	if request.method=="POST" and not request.is_ajax():
		if form_selected.is_valid(): # Compare button
			render(request, 'Home/compare.html', {'selected_boards': form_selected.cleaned_data[selected_boards]})

	return render(request, 'Home/search.html',{'form_search': form_search, 'form_results' : form_results, 'form_selected': form_selected})

@csrf_exempt
def post(request):
	# This is where the ajax request should redirect for the submission of the SearchBox form...
	if request.method=="POST":
		if request.is_ajax():
			print "AJAX Posted!"
			# grabs the ugly data stream taht is returned from the post
			search_data = request.POST.get('search_input', '')

			# THERE MUST BE A BETTER WAY TO DO THIS...BUT AT LEAST I HAVE THE DATA
			#print "Search Input: " + search_data
			cleaned_search_input = search_data.split("search_input=")[1].replace('%20',' ')
			print cleaned_search_input
			form_results = SearchResults()
			form_results.fields['search_output'].queryset = dbBoards.objects.filter(name__contains=cleaned_search_input)
			
			html = render_to_string('Home/search.html', {'form_results': form_results})

			return HttpResponse(html)
	return HttpResponse('')

def compare(request):
	return render(request,'Home/compare.html')