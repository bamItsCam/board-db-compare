from django.shortcuts import render
from django.http import HttpResponse
from .models import dbBoards
from django.core.management import call_command

#call_command('populate_db') This currently takes a lot of time...I think it should only be run once a week or something

#This method is called each time the user goes to the root url of the home page (see home/urls.py)
def index(request):
	#Grabs the first 50 boards from the dbBoards database
	first_50_boards = dbBoards.objects.all()[:50]
	#Sends the resulting dictionary of boards to the home.html file that contains the Home page content
	return render(request,'Home/home.html', {'boards': first_50_boards})
