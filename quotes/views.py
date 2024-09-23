# quotes/views.py
#description: write view functions to handle URL requests for the quotes app
from django.shortcuts import render

# Create your views here.

import random


quotes = [
    "“My life is proof that no matter what situation you're in, as long as you have a supportive family, you can achieve anything.”",
    "“We were blessed, and with blessing comes responsibility.”",
    "“Never be afraid to be a poppy in a field of daffodils”", 
]

images = [
    "/static/deprince1.jpg",  
    "/static/deprince2.jpg",
    "/static/deprince3.jpg"
]


#  Main page
def base(request):
    template_name = 'quotes/base.html'
    return render(request, template_name)

#view for the quotes page
def quote(request):
    selected_quote = random.choice(quotes)
    selected_image = random.choice(images)
    template_name = 'quotes/quote.html'
    return render(request, template_name, {'quote': selected_quote, 'image': selected_image})

# View to show all quotes and images
def show_all(request):
    template_name = 'quotes/show_all.html'
    return render(request, template_name, {'quotes': quotes, 'images': images})

# View for the about page
def about(request):
    template_name = 'quotes/about.html'
    return render(request, template_name)