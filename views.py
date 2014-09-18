# -*- coding: UTF-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template import Context
#import datetime

from books_management.models import User, Book

# define the logic of your apps here
	
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
	dict = {}
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
	return render_to_response('register.html', Context(dict))

def user_search(request):
	dict = {}
	if request.POST:
		post = request.POST
		book_list = Book.objects.get(bookname = post['bookname'])	
	return render_to_response('user_search.html', Context(dict))

def show_userinfo(request):
	dict = {}
	if request.POST:
		post = request.POST
	pass

def manager_search(request):
	issend = False
	dict = {}
	if request.POST:
		issend = True
		post = request.POST
		dict['book_list'] = Book.objects.filter(bookname = post['bookname'])
	dict['issend'] = issend
	return render_to_response('manager_search.html', Context(dict))
	
def newbookentering(request):
	isenter = False
	ismatch = False
	dict = {}
	if request.POST:
		isenter = True
		post = request.POST
		if len(post['isbn']) == 13:
			ismatch = True
			new_book = Book(
				isbn = post['isbn'],
				bookname = post['bookname'],
				number = post['number'],
				authorname = post['authorname'],
				booktype = post['booktype'],
				callnumber = post['callnumber'],
				publisher = post['publisher'],
				puclishtime = post['puclishtime'],
				price = post['price'],
			)
			new_book.save()
	dict['isenter'] = isenter
	dict['ismatch'] = ismatch
	return render_to_response('newbookentering.html', Context(dict))
	
	
	