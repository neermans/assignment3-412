from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm 
from .forms import CreateDancerProfileForm, CreateRecruiterProfileForm
from .models import DancerProfile, RecruiterProfile

# Create your views here.


class CreateDancerProfileView(CreateView):
    model = DancerProfile
    form_class = CreateDancerProfileForm
    template_name = 'project/create_dancer_profile_form.html'

    def get_success_url(self) -> str:
        return reverse('show_dancer_profile', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            form.instance.user = new_user
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))
        

class DancerProfileListView(ListView):
    model = DancerProfile
    template_name = 'project/dancer_profile_list.html'
    context_object_name = 'profiles'

class DancerProfileDetailView(DetailView):
    model = DancerProfile
    template_name = 'project/dancer_profile_detail.html'
    context_object_name = 'profile'



class CreateRecruiterProfileView(CreateView):
    model = RecruiterProfile
    form_class = CreateRecruiterProfileForm
    template_name = 'project/create_recruiter_profile_form.html'

    def get_success_url(self):
        # Adjust the URL name based on your actual URL configuration
        return reverse('show_recruiter_profile', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        if 'profile_form' not in context:
            context['profile_form'] = self.get_form()
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            form.instance.user = new_user
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))