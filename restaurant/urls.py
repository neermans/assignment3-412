# restaurant/urls.py
# define the URL patterns for the restaurant app

from django.urls import path
from django.conf import settings
from . import views

# define a list of valid URL patterns
# /main : Main page of the restaurant with the information including name, hours of operation, location, and pictures.
# /order : Online ordering form (details of page made in html templates).
# /confirmation : a confirmation page to show to the customer after an order has been placed. 
#       shows which items were ordered, customer infor, when food will be ready for pickup
#       The confirmation page will display which items were ordered, the customer information, 

urlpatterns = [
    path('', views.main, name='main'), 
    path('main/', views.main, name='main'),
    path('order/', views.order, name='order'),
    path('confirmation/', views.confirmation, name='confirmation'),
]