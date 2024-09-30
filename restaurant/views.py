# restaurant/views.py
# Define the views for the restaurant app

from django.shortcuts import render, redirect
import random
import time
from datetime import timedelta, datetime 

# Create your views here.

def main(request):
    '''
    Main page about the restaurant. 
    displays the main.html template that i made.
    '''

    template_name = "restaurant/main.html"

    return render(request, template_name)


def order(request):
    '''
    Ordering page for the restaurant. 
    Includes the list of options to order with their prices as well as a daily special
    displays the order.html template that was made.
    '''
    template_name = "restaurant/order.html"

    # list of specials 
    specials = [
        'Corn Bread','Baked Macaroni and Cheese','Pimento Cheese Spread','Pecan Pie','Blueberry Cobbler','Biscuits and Gravy','Pumpkin Bread','Fruit Cake','Strawberry Shortcake','Peanut Brittle','Bananas Foster','Banana Pudding','Bread Pudding','Alligator','Crab Cakes','Crawfish','Pork Chops','Fried Pork Chops','Turkey','Fried Turkey','Ham','Jambalaya','Fried Shrimp','Po` boy','Tomato Sandwich','Coleslaw'
    ]

        # list of specials 
    menu_prices = {
        'Corn Bread': 4.00,
        'Baked Macaroni and Cheese': 11.99,
        'Pimento Cheese Spread': 5.99,
        'Pecan Pie': 8.00,
        'Blueberry Cobbler': 8.00,
        'Biscuits and Gravy': 14.99,
        'Pumpkin Bread': 8.00,
        'Fruit Cake': 8.00,
        'Strawberry Shortcake': 8.00,
        'Peanut Brittle': 8.00,
        'Bananas Foster': 8.00,
        'Banana Pudding': 8.00,
        'Bread Pudding': 8.00,
        'Alligator': 15.99,
        'Crab Cakes': 15.99,
        'Crawfish': 15.99,
        'Pork Chops': 14.00,
        'Fried Pork Chops': 15.99,
        'Turkey': 14.00,
        'Fried Turkey': 15.99,
        'Ham': 12.99,
        'Jambalaya': 16.00,
        'Fried Shrimp': 13.99,
        'Po` boy': 16.00,
        'Tomato Sandwich': 9.99,
        'Coleslaw':  4.00,
    }

    daily_special = specials[random.randint(0, len(specials)-1)]
    daily_special_price = menu_prices[daily_special]

    context = {
        'daily_special': daily_special,
        'daily_special_price': daily_special_price
    }

    return render(request, template_name, context)

def confirmation(request):
    '''
    Confirmation page of the order after it is placed
    This view checks in with the form data that was submitted to check off which food items were ordered
    these items will then be added to the confirmation page for the customer to see what they ordered 
    We then calculate the total price that the customer owes
    displays the confirmation.html page
    '''

    template_name = 'restaurant/confirmation.html'

    # menu prices again
    menu_prices = {
        'Corn Bread': 4.00,
        'Baked Macaroni and Cheese': 11.99,
        'Pimento Cheese Spread': 5.99,
        'Pecan Pie': 8.00,
        'Blueberry Cobbler': 8.00,
        'Biscuits and Gravy': 14.99,
        'Pumpkin Bread': 8.00,
        'Fruit Cake': 8.00,
        'Strawberry Shortcake': 8.00,
        'Peanut Brittle': 8.00,
        'Bananas Foster': 8.00,
        'Banana Pudding': 8.00,
        'Bread Pudding': 8.00,
        'Alligator': 15.99,
        'Crab Cakes': 15.99,
        'Crawfish': 15.99,
        'Pork Chops': 14.00,
        'Fried Pork Chops': 15.99,
        'Turkey': 14.00,
        'Fried Turkey': 15.99,
        'Ham': 12.99,
        'Jambalaya': 16.00,
        'Fried Shrimp': 13.99,
        'Po` boy': 16.00,
        'Tomato Sandwich': 9.99,
        'Coleslaw':  4.00,
        'Fried Chicken Plate':  19.00,
        'Collard Greens': 7.99,
        'Fried Catfish': 15.00,
        'Grits': 10.99,
        'Potato Casserole': 14.00,

    }
    

    # ensure that there is a POST request
    if request.POST:


        # covnert to python
        name = request.POST['name']
        # items ordered
        items = request.POST.getlist('items')
        amount_owed = 0

        # total price
        for item in items:
            if item in menu_prices:
                amount_owed += menu_prices[item]
                amount_owed = round(amount_owed, 2)

        # generate time order will be ready
        ready_time = datetime.now() + timedelta(minutes=random.randint(30, 60))
        
        context = {
            'name' : name,
            'ordered_items': items,
            'amount_owed': amount_owed,
            'ready_time': ready_time.strftime('%I:%M %p'),
        }

        return render(request, template_name, context)
    
    ## GET request 
    # redirect to order URL:
    return redirect('order')

