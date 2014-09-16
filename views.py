from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import Context
import datetime

from books_management.models import People, User, Book

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
	if request.POST:
		post = request.POST
		user = User.objects.get(email = post['email'], passwd = post['passwd'])
		if len(user) == 1:
			ismatch = True
	c = Context({'ismatch': ismatch, 'email': request.POST.get('email', '-'), })
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
				new_user = User(email = post['email'], name = post['name'], passwd = post['passwd'], )
				new_user.save()
	c = Context({'exist' : exist, 'same' : same, })
	return render_to_response('register.html', c)

def findbook(request):
	if request.POST:
		post = request.POST
		book_list = Book.objects.get(bookname = post['bookname'])		
	c = Context({'book_list' : book_list, })
	return render_to_response('borrower_main.html', c)
	
	
	
	