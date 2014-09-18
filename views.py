# -*- coding: UTF-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
import datetime

from books_management.models import User, Book

# define the logic of your apps here

def insert(request):
	issend = False
	
	if request.POST:
		issend = True
		post = request.POST
		new_user = User(account = post['account'], passwd = post['passwd'])
		new_user.save()
	if issend:
		#user_list = User.objects.all()
		#c = Context({'account':user_list[0].account})
		user = request.POST.get('account')
		print type(user)
		c = Context({'account':user})
	else:
		c = Context({'account':'xxx'})
	return render_to_response('insert.html', Context(dict))
	
def list(request):
	people_list = People.objects.all()
	c = Context({'people_list' : people_list})
	return render_to_response('list.html', c)
	
def login(request):
	issend = False
	ismatch = False
	dict = {}
	if request.POST:
		issend = True
		post = request.POST
		user = User.objects.filter(account = post['account'], passwd = post['passwd']).first()
		if user:
			ismatch = True
			dict['account'] = user.account
	dict['issend'] = issend
	dict['ismatch'] = ismatch
	if ismatch:
		if dict['account'] != 'root':
			return HttpResponseRedirect('../user_search')
		return HttpResponseRedirect('../manager_search')
	return render_to_response('login.html', Context(dict))

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

def user_search(request):
	dict = {}
	if request.POST:
		post = request.POST
		book_list = Book.objects.get(bookname = post['bookname'])	
	return render_to_response('user_search.html', Context(dict))

def show_userinfo(request):
	pass

def manager_search(request):
	dict = {}
	if request.POST:
		post = request.POST
		book_list = Book.objects.get(bookname = post['bookname'])	
	return render_to_response('manager_search.html', Context(dict))
	
