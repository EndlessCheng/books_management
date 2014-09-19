# -*- coding: UTF-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template import Context
from books_management.models import User, Book

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
			return HttpResponseRedirect('../user_search') # 怎么把账户传进去？？
		return HttpResponseRedirect('../manager_search')
	return render_to_response('login.html', Context(dict))

def search(request):
	issend = False
	isborrow = False
	hadborrow = False
	dict = {}
	if request.POST: # if request.method == 'POST':
		issend = True
		post = request.POST
		if post.get('bookname'):
			book_list = list(Book.objects.filter(bookname__contains = post['bookname']))
			book_list.extend(list(Book.objects.filter(authorname__contains = post['bookname'])))
			book_list.extend(list(Book.objects.filter(callnumber__contains = post['bookname'])))
			book_list.extend(list(Book.objects.filter(publisher__contains = post['bookname'])))
			book_list = list(set(book_list))
			dict['book_list'] = book_list
			dict['size'] = len(book_list)
		else:
			# borrow, and decrease the number of book(s)
			# NOTE: can't borrow the same book again
			
			borrow_list = post.getlist('borrow_list')
			isborrow = True	
			had_borrow_list = []
			for booknm in borrow_list:
				if Borrow.objects.get(account = post['account'], bookname = booknm): # None ???
					had_borrow_list.append(book.bookname)
					isborrow = False
					hadborrow = True
			if hadborrow:
				dict['had_borrow_list'] = had_borrow_list
			else:
				for booknm in borrow_list:
					book = Book.objects.get(bookname = booknm)
					book.number -= 1
					book.save()
			dict['borrow_list'] = borrow_list
	dict['issend'] = issend
	dict['isborrow'] = isborrow
	dict['hadborrow'] = hadborrow
	return dict

def user_search(request):
	return render_to_response('user_search.html', Context(search(request)))
	
def manager_search(request):
	return render_to_response('manager_search.html', Context(search(request)))

def show_userinfo(request):
	dict = {}
	if request.POST:
		post = request.POST
	pass

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
	
	
	