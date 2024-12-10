from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView, FormView
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .forms import *
from .models import *
from django.db.models import Q

# Create your views here.

class BlogHomeView(TemplateView):
    template_name = 'project/blog_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch posts for videos and music
        context['dance_posts'] = DancePost.objects.filter(
            Q(video__isnull=False) | Q(cut_music__isnull=False)
        ).order_by('-created_at')  # Combine videos and music

        # Fetch general posts from the CommentBoardPost model
        context['general_posts'] = CommentBoardPost.objects.filter(
            post_type=CommentBoardPost.PostType.GENERAL
        ).order_by('-id')  # Order by newest first

        return context
   
class CreateDancerProfileView(CreateView):
    model = DancerProfile
    form_class = CreateDancerProfileForm
    template_name = 'project/create_dancer_profile_form.html'

    def get_success_url(self) -> str:
        return reverse('dancer_profile_detail', kwargs={'pk': self.object.pk})

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
            form.instance.dancerUser = new_user
            return super().form_valid(form)
        else:
            # If user form has errors, re-render the template with errors
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))
        

class ProfileListView(TemplateView):
    template_name = 'project/profile_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dancers'] = DancerProfile.objects.all()  # Query all dancers
        context['recruiters'] = RecruiterProfile.objects.all()  # Query all recruiters
        return context

class DancerProfileDetailView(LoginRequiredMixin, DetailView):
    model = DancerProfile
    template_name = 'project/dancer_profile_detail.html'
    context_object_name = 'profile'


class CreateRecruiterProfileView(CreateView):
    model = RecruiterProfile
    form_class = CreateRecruiterProfileForm
    template_name = 'project/create_recruiter_profile_form.html'

    def get_success_url(self):
        # Adjust the URL name based on your actual URL configuration
        return reverse('recruiter_profile_detail', kwargs={'pk': self.object.pk})

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
            form.instance.recruiterUser = new_user
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))
        

class RecruiterProfileDetailView(LoginRequiredMixin, DetailView):
    model = RecruiterProfile
    template_name = 'project/recruiter_profile_detail.html'
    context_object_name = 'profile'

class SendMessageView(LoginRequiredMixin, FormView):
    template_name = 'project/send_message.html'
    form_class = PrivateMessageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receiver_id = self.kwargs['receiver_id']
        receiver = get_object_or_404(User, pk=receiver_id)

        # Add receiver profiles to context
        context['receiver'] = receiver
        context['dancer_profile'] = getattr(receiver, 'dancer_profile', None)
        context['recruiter_profile'] = getattr(receiver, 'recruiter_profile', None)

        # Fetch messages between the logged-in user and the receiver
        context['messages'] = PrivateMessage.objects.filter(
            Q(sender=self.request.user, receiver=receiver) |
            Q(sender=receiver, receiver=self.request.user)
        )
        return context

    def form_valid(self, form):
        receiver_id = self.kwargs['receiver_id']
        receiver = get_object_or_404(User, pk=receiver_id)

        # Prevent sending a message to yourself
        if receiver == self.request.user:
            if hasattr(receiver, 'dancer_profile'):
                return redirect('dancer_profile_detail', pk=receiver.dancer_profile.pk)
            elif hasattr(receiver, 'recruiter_profile'):
                return redirect('recruiter_profile_detail', pk=receiver.recruiter_profile.pk)

        # Save the new message
        form.instance.sender = self.request.user
        form.instance.receiver = receiver
        form.save()

        # Redirect back to the same messaging page
        return redirect('send_message', receiver_id=receiver.pk)
    


class EditRecruiterProfileView(LoginRequiredMixin, UpdateView):
    model = RecruiterProfile
    fields = ['name', 'dance_company', 'email_contact', 'image']
    template_name = 'project/edit_recruiter_profile.html'

    def dispatch(self, request, *args, **kwargs):
        # Ensure the logged-in user matches the profile owner
        profile = self.get_object()
        if profile.recruiterUser != request.user:
            return redirect('recruiter_profile_detail', pk=profile.pk)  # Redirect to profile detail if not authorized
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()


class EditDancerProfileView(LoginRequiredMixin, UpdateView):
    model = DancerProfile
    fields = ['name', 'preferred_styles', 'bio', 'job_history', 'image']
    template_name = 'project/edit_dancer_profile.html'

    def dispatch(self, request, *args, **kwargs):
        # Ensure the logged-in user matches the profile owner
        profile = self.get_object()
        if profile.dancerUser != request.user:
            return redirect('dancer_profile_detail', pk=profile.pk)  # Redirect to profile detail if not authorized
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()
    


class CreateDancePostView(LoginRequiredMixin, CreateView):
    model = DancePost
    fields = ['video', 'cut_music', 'description']
    template_name = 'blog/create_dance_post.html'

    def form_valid(self, form):
        # Ensure the logged-in user has a DancerProfile
        try:
            dancer_profile = self.request.user.dancer_profile
        except DancerProfile.DoesNotExist:
            return redirect('error_page')  # Replace with a proper error page or message
        # Assign the logged-in user's DancerProfile as the poster
        form.instance.poster = dancer_profile
        return super().form_valid(form)

    def get_success_url(self):
        return redirect('blog_home')  # Replace with the desired success redirect URL
    


class CreateCommentBoardPostView(LoginRequiredMixin, CreateView):
    model = CommentBoardPost
    fields = ['content', 'post_type']
    template_name = 'blog/create_comment_post.html'

    def form_valid(self, form):
        # Assign the logged-in user as the author
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return redirect('blog_home')  # Replace with the desired success redirect URL