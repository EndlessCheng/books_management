# -*- coding: UTF-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template import Context
from books_management.models import User, Book, Borrow, OnlineUser, Fine
from decimal import Decimal
# from django.utils import timezone

from datetime import datetime, timedelta


def login(request):
    issend = False
    ismatch = False
    dict = {}
    if request.POST:
        issend = True
        post = request.POST
        user = User.objects.filter(account=post['account'], passwd=post['passwd']).first()
        if user:
            ismatch = True
            dict['account'] = user.account
    dict['issend'] = issend
    dict['ismatch'] = ismatch
    if ismatch:
        # update the unique online user
        onlineuser_list = OnlineUser.objects.all()
        for onlineuser in onlineuser_list:
            onlineuser.delete()
        new_onlineuser = OnlineUser(account=User.objects.filter(account=post['account'], passwd=post['passwd']).first())
        new_onlineuser.save()
        # update end
        admin_account_name = ["admin", "root"]
        for name in admin_account_name:
            if post['account'] == name:
                return HttpResponseRedirect('../manager_search')
        return HttpResponseRedirect('../user_search')
    return render_to_response('login.html', Context(dict))


def search(request):
    issend = False
    isborrow = False
    hadborrow = False
    exceedmax = False
    onlineuser = list(OnlineUser.objects.all())[0].account
    dict = {'onlineuser': onlineuser.account}
    maxbooknumber = 8
    if request.POST:  # if request.method == 'POST':
        issend = True
        post = request.POST
        if post.get('bookname'):
            if post['bookname'] == '-all':
                book_list = list(Book.objects.all())
            else:
                book_list = list(Book.objects.filter(bookname__contains=post['bookname']))
                book_list.extend(list(Book.objects.filter(authorname__contains=post['bookname'])))
                book_list.extend(list(Book.objects.filter(callnumber__contains=post['bookname'])))
                book_list.extend(list(Book.objects.filter(publisher__contains=post['bookname'])))
                book_list = list(set(book_list))
            dict['book_list'] = book_list
            dict['size'] = len(book_list)
        else:  # decrease the number of book(s), and borrow
            borrow_list = post.getlist('borrow_list')
            isborrow = True
            had_borrow_list = []
            for booknm in borrow_list:  # can't borrow the same book again
                if Borrow.objects.filter(account=User.objects.filter(account=onlineuser.account).first(),
                                         isbn=Book.objects.filter(bookname=booknm).first()):
                    had_borrow_list.append(booknm)
                    isborrow = False
                    hadborrow = True
            if hadborrow:
                dict['had_borrow_list'] = had_borrow_list
            else:
                if len(list(borrow_list)) + len(list(Borrow.objects.filter(
                        account=User.objects.filter(account=onlineuser.account).first()))) <= maxbooknumber:
                    for booknm in borrow_list:
                        book = Book.objects.get(bookname=booknm)
                        book.number -= 1
                        book.save()
                        nowtime = datetime.now()
                        new_borrow = Borrow(
                            account=onlineuser,
                            isbn=Book.objects.filter(bookname=booknm).first(),
                            begintime=nowtime,
                            endtime=nowtime + timedelta(days=30),
                            realtime=nowtime,
                        )
                        new_borrow.save()
                else:
                    exceedmax = True
                    isborrow = False
            dict['borrow_list'] = borrow_list
    dict['issend'] = issend
    dict['isborrow'] = isborrow
    dict['hadborrow'] = hadborrow
    dict['exceedmax'] = exceedmax
    dict['maxbooknumber'] = maxbooknumber
    return dict


def user_search(request):
    return render_to_response('user_search.html', Context(search(request)))


def manager_search(request):
    return render_to_response('manager_search.html', Context(search(request)))


def show_mybook(request):
    # issend = False
    onlineuser = list(OnlineUser.objects.all())[0].account
    dict = {'onlineuser': onlineuser.account}
    if request.POST:
        # issend = True
        post = request.POST
        renewbook_list = post.getlist('renewbook_list')
        dict['renewbook_list'] = renewbook_list
        dict['renewbook_list_size'] = len(renewbook_list)
        for booknm in renewbook_list:
            borrow = Borrow.objects.filter(account=onlineuser,
                                           isbn=Book.objects.filter(bookname=booknm).first()).first()
            borrow.endtime += timedelta(days=30)
            borrow.add += 1
            borrow.save()
        #
        returnbook_list = post.getlist('returnbook_list')
        dict['returnbook_list'] = returnbook_list
        dict['returnbook_list_size'] = len(returnbook_list)
        nowtime = datetime.now()
        for booknm in returnbook_list:
            borrow = Borrow.objects.filter(account=onlineuser,
                                           isbn=Book.objects.filter(bookname=booknm).first()).first()
            if borrow:
                borrow.delete()
                if nowtime.date() > borrow.endtime.date():
                    delta = nowtime.date() - borrow.endtime.date()
                    tmp_fine = Fine.objects.filter(account=onlineuser).first()
                    if tmp_fine:
                        tmp_fine.fine += Decimal(0.5 * delta.days)
                        tmp_fine.save()
                    else:
                        new_fine = Fine(account=onlineuser, fine=0.5 * delta.days, dealtime=nowtime)
                        new_fine.save()
                book = Book.objects.get(bookname=booknm)
                book.number += 1
                book.save()
    borrow_list = list(Borrow.objects.filter(account=onlineuser))
    dict['borrow_list'] = borrow_list
    dict['borrow_list_size'] = len(borrow_list)
    return render_to_response('mybook.html', Context(dict))


def show_userinfo(request):
    onlineuser = list(OnlineUser.objects.all())[0].account
    issend = False
    ismatch = False
    dict = {'onlineuser': onlineuser}
    if request.POST:
        issend = True
        post = request.POST
        user = User.objects.filter(account=onlineuser.account, passwd=post['passwd']).first()
        if user and post['newpasswd'] == post['renewpasswd']:
            ismatch = True
            user.passwd = post['newpasswd']
            user.save()
    dict['issend'] = issend
    dict['ismatch'] = ismatch
    return render_to_response('userinfo.html', Context(dict))


def newbookentering(request):
    isenter = False
    isfull = True
    ismatch = False
    isbnlength = 13
    dict = {}
    if request.POST:
        isenter = True
        post = request.POST
        post_name_list = ['isbn', 'bookname', 'number', 'authorname', 'booktype', 'callnumber', 'publisher',
                          'puclishtime', 'price']
        for post_name in post_name_list:
            if post[post_name] == '':
                isfull = False
                break
        if isfull and len(post['isbn']) == isbnlength:
            ismatch = True
            new_book = Book(
                isbn=post['isbn'],
                bookname=post['bookname'],
                number=post['number'],
                authorname=post['authorname'],
                booktype=post['booktype'],
                callnumber=post['callnumber'],
                publisher=post['publisher'],
                puclishtime=post['puclishtime'],
                price=post['price'],
            )
            new_book.save()
    dict['isenter'] = isenter
    dict['isfull'] = isfull
    dict['ismatch'] = ismatch
    dict['isbnlength'] = isbnlength
    return render_to_response('newbookentering.html', Context(dict))


def show_all_borrow(request):
    issend = False
    borrow_list = list(Borrow.objects.all())
    dict = {'borrow_list': borrow_list, 'borrow_list_size': len(borrow_list)}
    return render_to_response('all_borrow.html', Context(dict))


def dealfine(request):
    issend = False
    dict = {}
    if request.POST:
        issend = True
        post = request.POST
        deal_list = post.getlist('deal_list')
        dict['deal_list'] = deal_list
        dict['deal_list_size'] = len(deal_list)
        for accountnm in deal_list:
            fine = Fine.objects.filter(account=User.objects.filter(account=accountnm).first()).first()
            fine.delete()
    dict['issend'] = issend
    fine_list = list(Fine.objects.all())
    dict['fine_list'] = fine_list
    dict['fine_list_size'] = len(fine_list)
    return render_to_response('dealfine.html', Context(dict))
