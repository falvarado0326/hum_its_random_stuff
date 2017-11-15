from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),    
    url(r'^quotes$', views.quotes),    
    url(r'^users/(?P<id>\d+)$', views.user),
    url(r'^quotes/add$', views.add_quote),     
    url(r'^quotes/favorite', views.add_favorite), 
    url(r'^quotes/remove_favorite', views.remove_favorite), 
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
]