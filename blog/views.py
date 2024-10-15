# blog/views.py
# define the views for the blog app
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import * # import all of the models (e.g. Article)
from blog.forms import * #import the forms (CreateCommentForm)
from django.urls import reverse

import random

# class-based view
class ShowAllView(ListView):
    ''' the view to show all Articles '''
    model = Article # the model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # context variable to use in the template



class RandomArticleView(DetailView):
    '''display one Article selected at Random'''
    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    def get_object(self):
        '''return one article chosen at random'''

        # retrieve all of the articles
        all_articles = Article.objects.all()

        # pick one at random and return it 
        article = random.choice(all_articles)
        return article


class ArticleView(DetailView):
    '''display one Article selected at Random'''
    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"
    
   
class CreateCommentView(CreateView):
    ''' a view to create a comment on an article'''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self) -> str:
        '''return the URL tg to redirect on success'''
        #return reverse('show_all')
        return reverse('article', kwargs=self.kwargs)


    
    def form_valid(self, form):
        '''this method is called after the form is validated,
        before saving data to the database '''

        print(f'CreateCommentView.form_valid() form={form.cleaned_data}')
        print(f'CreateCommentView.form_valid() self.kwargs={self.kwargs}')

        # find the article identified by the PK from the URL pattern
        article = Article.objects.get(pk=self.kwargs('pk'))

        # attach the Article to the instance of the comment to set its FK
        form.instance.article = article #like saying comment.article = article

        #delegate work to superclass 
        return super().form_valid(form)