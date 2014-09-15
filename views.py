from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import Context
import datetime

from books_management.models import People

def hello(request):
	return HttpResponse("Welcome to books management!")
	
def current_time(request):
	now = datetime.datetime.now()
	return HttpResponse(now)
	
def current_time_in_html(request):
	now = datetime.datetime.now()
	c = Context({'time':now})
	return render_to_response("time.html", c)
	
def insert(request):
	if request.POST:
		post = request.POST
		new_people = People(name = post['name'], sex = (post['sex'] == 'M'), email = post['email'])
		new_people.save()
	return render_to_response('insert.html')