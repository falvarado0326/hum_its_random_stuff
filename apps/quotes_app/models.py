# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import UserManager
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt

class UserManager(models.Manager):

  def login(self, POST):
    errors = []
    if len(self.filter(email=POST['email'])) > 0:            
        user = self.get(email=POST['email'])
        if not bcrypt.checkpw(POST['password'].encode(), user.password.encode()):
            errors.append('email/password incorrect')
    else:
        errors.append('email/password incorrect')

    if len(errors)>0:
        return (False, errors)
    else:
        
        return (True, user)

  def validate(self, POST):
    errors = []
    if len(POST['name'])<2:
        errors.append('First name is required!')
    if len(POST['alias'])<2:
        errors.append('Alias is required!')
    if len(POST['email'])<2:
        errors.append('Email is required!') 
    elif not EMAIL_REGEX.match(POST['email']):
        errors.append('Email is not valid!')     
    elif len(User.objects.filter(email = POST['email']))>0:
        errors.append('Email already exists!')
    if len(POST['password'])<9:
        errors.append('Password cannot be under 8 characters!') 
    elif POST['c_password'] != POST['password']:
        errors.append('Password does not match!')
    if len(errors)>0: 
      return (False, errors)
    else:
        new_user = User.objects.create(
            name = POST['name'],
            alias = POST['alias'],
            email = POST['email'],
            password = bcrypt.hashpw(POST['password'].encode(), bcrypt.gensalt())
        ) 
        return (True, new_user)

class User(models.Model):
      name = models.CharField(max_length=255)
      alias = models.CharField(max_length=255)
      email = models.CharField(max_length=255)
      password = models.CharField(max_length=255)
      objects = UserManager()
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)

class QuoteManager(models.Manager):
    def validate(self, POST):
        errors = []
        if len(POST['author'])<2:
            errors.append('The "Quoted By" is empty!')
        if len(POST['quote'])<2:
            errors.append('The "Message" is empty!')
        if len(errors)>0: 
            return (False, errors)
        else:
            user = User.objects.get(id=POST['user'])
            new_quote = Quote.objects.create(
                author = POST['author'],
                quote = POST['quote'],
                user =  user               
            )
             
            return (True, new_quote)

class Quote(models.Model):
    author = models.CharField(max_length=255)
    quote = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="quotes") 
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = QuoteManager()

class FavoriteManager(models.Manager):
    def create_favorite(self, POST):
        user = User.objects.get(id=POST['user'])
        quote = Quote.objects.get(id=POST['quote'])
        favorite = Favorite.objects.create(
            quote = quote,
            user =  user               
        )            
        return (favorite)
    def remove_favorite(self, POST):
        user = User.objects.get(id=POST['user'])
        quote = Quote.objects.get(id=POST['quote'])
        favorite = Favorite.objects.filter(
            quote = quote,
            user =  user               
        ) 
        favorite.delete()
        return (favorite)
class Favorite(models.Model):
    quote = models.ForeignKey(Quote, related_name="favorite")
    user = models.ForeignKey(User, related_name="favorited_by")
    objects = FavoriteManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
