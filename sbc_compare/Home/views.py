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
#TODO: logging, with an ip address of the user (django-ipware)
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

	# compare button check
	if request.method=="POST" and "compare" in request.POST:
		return _compare_button_press(request)
	# Reset button check
	elif request.method=="POST" and "reset" in request.POST:
		return _reset_button_press(request)

	# allow the user to come back to what they were doing, even after a refresh
	# therefore update the forms with session data
	form_search.fields['search_input'].initial = request.session.get('latest_search', '')
	form_results = _update_results_form(request)
	form_selected = _update_selected_form(request)
	
	return render(request, 'Home/search.html',{'form_search': form_search, 'form_results' : form_results, 'form_selected': form_selected})

def search_post(request):
	if request.method=="POST" and request.is_ajax():
		print "AJAX Search!"

		# parse the ugly data stream that is returned from the post
		request.session['latest_search'] = request.POST.get('search_input', '').split("search_input=")[1].replace('%20',' ')
		
		# Update forms and other template content
		form_results = _update_results_form(request)
		search_count = _count_search_results(request)

		return TemplateResponse(request, 'Home/search.html', {'form_results': form_results, 'search_count': search_count})
	return HttpResponse('')

def add_post(request):
	if request.method=="POST" and request.is_ajax():
		print "AJAX Add!"

		# grabs the ids of all the boards to be added to the compare list
		request.session['all_selected_board_ids'] = _clean_added_boards_string(request.POST.get('added_boards', ''))

		# Update forms
		form_results = _update_results_form(request)
		form_selected = _update_selected_form(request)

		return TemplateResponse(request, 'Home/search.html', {'form_results': form_results, 'form_selected': form_selected})
	return HttpResponse('')

def compare(request):
	selected = _reformat_board_attributes(request.session.get('selected', ''))

	return render(request,'Home/compare.html',{'selected' : selected})

# "Private" functions
def _compare_button_press(request):
	form_results = SearchResults(request.POST)
	if form_results.is_valid(): # Compare button
		request.session['selected'] = list(form_results.cleaned_data['search_output'].values())
		print "compare hit"
		return redirect('/compare')

def _reset_button_press(request):
	# clear session vals
	request.session['latest_search'] = ''
	request.session['all_selected_board_ids'] = ''
	print "reset hit"
	return redirect('/search')

def _count_search_results(request):
	count = dbBoards.objects.filter(name__contains=request.session.get('latest_search', '')).count()
	if count == 0:
		return 'No boards found!'
	elif count == 1:
		return '1 board was found'
	else:
		return '%d boards were found' %(count)

def _clean_added_boards_string(rawString):
	if 'search_output=' in rawString:
		cleanString = rawString.replace('&', '').split('search_output=')
	else:
		cleanString = rawString.replace('&', '').split('selected_boards=')

	# get rid of empty element
	cleanString.pop(0)

	return cleanString 

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
	thisForm.fields['selected_boards'].queryset = dbBoards.objects.filter(pk__in=request.session.get('all_selected_board_ids', ''))
	thisForm.fields['selected_boards'].initial = request.session.get('all_selected_board_ids', '')

	thisForm.fields['selected_boards'].empty_label=None

	return thisForm

def _update_results_form(request):
	thisForm = SearchResults()
	thisForm.fields['search_output'].queryset = dbBoards.objects.filter(Q(name__contains=request.session.get('latest_search', '')) | Q(pk__in=request.session.get('all_selected_board_ids', '')))
	thisForm.fields['search_output'].initial = request.session.get('all_selected_board_ids', '')
	thisForm.fields['search_output'].empty_label=None
	return thisForm