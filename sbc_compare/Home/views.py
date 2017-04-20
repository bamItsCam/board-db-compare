from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.db.models import Q
from django.shortcuts import redirect

from .models import dbBoards
from .forms import SelectBoards, SearchBox, SearchResults, SearchSelected
from django.core.management import call_command

#call_command('populate_db') This currently takes a lot of time...I think it should only be run once a week or something

def about(request):
	return render(request,'Home/about.html')

#Displays the SelectBoards form and allows the user to select boards. 
def select_boards(request):
	form = SelectBoards()
	if request.method == "POST":
		form = SelectBoards(request.POST)
		if form.is_valid():
			form_list = []
			form_data = form.cleaned_data['boards'].values()
			for item in form_data:
   				form_list.append(dict(item))
   			print form_list
			return render(request, 'Home/compare.html', {'selected': form_list})
	return render(request, 'Home/home.html',{'form':form})

def search_boards(request):
	form_search = SearchBox()
	form_results = SearchResults()
	form_selected = SearchSelected()
	form_selected.fields['selected_boards'].empty_label=None

	# compare button check
	if request.method=="POST" and "compare" in request.POST:
		print "here"
		form_results = SearchResults(request.POST)
		if form_results.is_valid(): # Compare button
			request.session['selected'] = list(form_results.cleaned_data['search_output'].values())
			print "*"
			print request.session['selected'] 
			return redirect('/compare')
	# Reset button check
	elif request.method=="POST" and "reset" in request.POST:
		# clear session vals
		request.session['latest_search'] = ''
		request.session['all_selected_board_ids'] = ''
		print "reset hit"
		return redirect('/search')

	# allow the user to come back to what they were doing, even after a refresh
	# therefore repopulate the forms with session data
	if 'latest_search' not in request.session:
			request.session['latest_search'] = ''
	form_search.fields['search_input'].initial = request.session['latest_search']
	print "Search: " + request.session['latest_search']

	if 'all_selected_board_ids' not in request.session:
		request.session['all_selected_board_ids'] = '' 

	# Make the SearchResults form what it was before a refresh
	form_results = _update_results_form(request)

	# Make the SearchSelected form what it was before a refresh
	form_selected = _update_selected_form(request)
	
	return render(request, 'Home/search.html',{'form_search': form_search, 'form_results' : form_results, 'form_selected': form_selected})

def search_post(request):
	# This is where the ajax request should redirect for the submission of the SearchBox form...
	if request.method=="POST" and request.is_ajax():
		print "AJAX Search!"
		# grabs the ugly data stream taht is returned from the post
		search_data = request.POST.get('search_input', '')

		if 'latest_search' not in request.session:
			request.session['latest_search'] = ''
		request.session['latest_search'] = search_data.split("search_input=")[1].replace('%20',' ')

		if 'all_selected_board_ids' not in request.session:
			request.session['all_selected_board_ids'] = ''

		# Update Search Results
		form_results = _update_results_form(request)

		# Check and alert if the search returned no results found
		count = dbBoards.objects.filter(name__contains=request.session['latest_search']).count()
		if count == 0:
			search_count = 'No boards found!'
		elif count == 1:
			search_count = '1 board was found'
		else:
			search_count = '%d boards were found' %(count)
		print search_count		
		return TemplateResponse(request, 'Home/search.html', {'form_results': form_results, 'search_count': search_count})
	return HttpResponse('')

def add_post(request):
	#TODO: clear latest search session on refresh
	#TODO: if query returns no results, say "no results found"

	# This is where the ajax request should redirect for the submission of the SearchBox form...
	if request.method=="POST" and request.is_ajax():
		print "AJAX Add!"
		
		# In order to update the search results and remove the chosen board, we need the original search string from the session
		if 'latest_search' not in request.session:
			request.session['latest_search'] = ''

		# grabs the ids of all the boards to be added to the compare list
		added_boards_raw = request.POST.get('added_boards', '')
		if 'search_output=' in added_boards_raw:
			added_boards_ids = added_boards_raw.replace('&', '').split('search_output=')
		else:
			added_boards_ids = added_boards_raw.replace('&', '').split('selected_boards=')

		# get rid of empty element
		added_boards_ids.pop(0)

		# use sessions to keep track of all selected boards
		if 'all_selected_board_ids' not in request.session:
			request.session['all_selected_board_ids'] = ''

		request.session['all_selected_board_ids'] = added_boards_ids 

		# Update Search Results
		form_results = _update_results_form(request)

		form_selected = _update_selected_form(request)
		return TemplateResponse(request, 'Home/search.html', {'form_results': form_results, 'form_selected': form_selected})
	return HttpResponse('')


def compare(request):
	selected = _reformat_board_attributes(request.session['selected'])

	return render(request,'Home/compare.html',{'selected' : selected})

def _reformat_board_attributes(thisSelected):
	for i in range(0,len(thisSelected)):
		for item in thisSelected[i]:
			if('unicode' in str(type(thisSelected[i][item]))):
				thisSelected[i][item] = (thisSelected[i][item]).replace(u'\ufffd','')
				thisSelected[i][item] = str((thisSelected[i][item]).encode("utf-8")).replace(';','<br />')
			elif('int' in str(type(thisSelected[i][item]))):
				thisSelected[i][item] = str(thisSelected[i][item]).replace(';','<br />') \
										.replace(':<br />',': ').replace(' , ',' ') \
										.replace('False-uid=jetfuelcantmeltsteelbeams','<span class="glyphicon glyphicon-remove"></span>') \
										.replace('False-uid=jetfuelcantmeltsteelbeams','<span class="glyphicon glyphicon-remove"></span>') \
										.replace('True-uid=jetfuelcantmeltsteelbeams','<span class="glyphicon glyphicon-ok"></span>') \
										.replace('Unknown-uid=jetfuelcantmeltsteelbeams','Unknown') \
										.replace('?','N/A')
	return thisSelected

def _update_selected_form(request):
	thisForm = SearchSelected()
	thisForm.fields['selected_boards'].queryset = dbBoards.objects.filter(pk__in=request.session['all_selected_board_ids'])
	thisForm.fields['selected_boards'].initial = request.session['all_selected_board_ids']

	thisForm.fields['selected_boards'].empty_label=None

	return thisForm

def _update_results_form(request):
	thisForm = SearchResults()
	thisForm.fields['search_output'].queryset = dbBoards.objects.filter( Q(name__contains=request.session['latest_search']) | Q(pk__in=request.session['all_selected_board_ids']) )
	thisForm.fields['search_output'].initial = request.session['all_selected_board_ids']
	thisForm.fields['search_output'].empty_label=None
	return thisForm