from __future__ import unicode_literals

from django.contrib import messages

from django.shortcuts import render, HttpResponse, redirect
  
from .models import User, Quote, Favorite

def index(request):
    return render(request, 'quotes_app/index.html')

def register(request):    
    result = User.objects.validate(request.POST)
    if result[0]:
        request.session['id'] = result[1].id
        return redirect('/')
    else:
        for error in result[1]:
            messages.add_message(request, messages.INFO, error)
        return redirect('/')

def login(request):
    result =  User.objects.login(request.POST)
    if result[0]: 
        print result[1]
        request.session['name'] = result[1].name 
        request.session['user_id'] = result[1].id 
        request.session['alias'] = result[1].alias 
        request.session['email'] = result[1].email 
        return redirect('/quotes')
    else:
        for error in result[1]:
            messages.add_message(request, messages.INFO, error)
        return redirect('/')

def quotes(request):
    context = {
        "user": User.objects.filter(id=request.session['user_id']),
        "quotes": Quote.objects.all(),
        "favorites": Favorite.objects.filter(user__id= request.session['user_id'])
        }    
    return render(request, 'quotes_app/quotes.html', context)

def add_quote(request):
    result = Quote.objects.validate(request.POST)
    if result[0]:
        return redirect('/quotes')
    else:
        for error in result[1]:
            messages.add_message(request, messages.INFO, error)
        return redirect('/quotes')
    return redirect('/quotes')

def user(request, id):
    context= {
        "users": User.objects.get(id=id),
        "quotes": Quote.objects.filter(user__id= id)
    }
    users= User.objects.get(id=id)
    print users
    return render(request, 'quotes_app/user.html', context)

def add_favorite(request):
    result = Favorite.objects.create_favorite(request.POST)
    return redirect('/quotes')

def remove_favorite(request):
    result = Favorite.objects.remove_favorite(request.POST)
    return redirect('/quotes')
def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')