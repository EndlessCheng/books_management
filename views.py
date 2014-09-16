from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import Context
import datetime

from books_management.models import People, User

# define the logic of your apps here

def hello(request):
	return HttpResponse("Welcome to books management!")
	
def current_time(request):
	now = datetime.datetime.now()
	return HttpResponse(now)
	
def current_time_in_html(request):
	now = datetime.datetime.now()
	c = Context({'time' : now})
	return render_to_response("time.html", c)
	
def insert(request):
	if request.POST:
		post = request.POST
		new_people = People(name = post['name'], sex = (post['sex'] == 'M'), email = post['email'])
		new_people.save()
	return render_to_response('insert.html')
	
def list(request):
	people_list = People.objects.all()
	c = Context({'people_list' : people_list, })
	return render_to_response('list.html', c)
	
def login(request):
	ismatch = False
	post = request.POST
	if post:
		user = User.objects.get(email = post['email'], passwd = post['passwd'])
		if len(user) == 1:
			ismatch = True
	c = Context({'ismatch': ismatch, }) #, 'email': post['email'][0]
	return render_to_response('login.html', c)	
	
def register(request):
	exist = False
	same = False
	if request.POST:
		post = request.POST
		if len(User.objects.get(email = post['email'])) == 1:
			exist = True
		else:
			if post['passwd'] == post['repeatpasswd']:
				same = True
			else:
				new_people = People(email = post['email'], name = post['name'], passwd = post['passwd'], )
				new_people.save()
	c = Context({'exist' : exist, 'same' : same, })
	return render_to_response('register.html', c)
