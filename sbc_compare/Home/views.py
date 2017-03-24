from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
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
	#if 'search_input' not in request.session:
	#	request.session['search_input'] = ''
	#print request.session['search_input']
	form_box = SearchBox()
	#form_results = SearchResults()
	#form_selected = SearchSelected()
	#if request.method == 'POST':
		#form_box = SearchBox(request.POST)
		#form_box.fields['search_input'].attrs = {'class': 'form-control','id': 'searchInput','value': request.session['search_input']}
		#if form_box.is_valid():
	#	request.session['search_input'] = request.POST.get('search_input', '') 
	#	form_results = SearchResults(request.POST)
	#	form_results.fields['search_output'].queryset = dbBoards.objects.filter(name__contains=request.session['search_input'])
	#	print "here"
	#	if form_results.is_valid():
			#search_output = request.POST.get('search_output', '')
	#		form_data = form_results.cleaned_data['search_output'].values()
	#		print "there"
	# I somehow need to pass a variable from the input into the form, maybe a second form?
	#return render(request, 'Home/search.html',{'form_box': form_box, 'form_results' : form_results})
	return render(request, 'Home/search.html',{'form_box': form_box})

@csrf_exempt
def post(request):
	# This is where the ajax request should redirect for the submission of the SearchBox form...
	if request.method=="POST":
		if request.is_ajax():
			print "AJAX Posted!"
			# grabs the ugly data stream taht is returned from the post
			search_data = str(request.POST.get('search_input'))

			# THERE MUST BE A BETTER WAY TO DO THIS...BUT AT LEAST I HAVE THE DATA
			print "Search Input: " + search_data.split("search_input=")[1].replace('%20',' ')
	return HttpResponse('')

def compare(request):
	return render(request,'Home/compare.html')