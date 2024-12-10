from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView, FormView, View
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .forms import *
from .models import *
from django.db.models import Q
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render


# Create your views here.

class BlogHomeView(TemplateView):
    template_name = 'project/blog_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch dance posts (videos and music)
        context['dance_posts'] = DancePost.objects.filter(
            Q(video__isnull=False) | Q(cut_music__isnull=False)
        ).order_by('-created_at')

        # Group CommentBoardPosts by type
        context['general_posts'] = CommentBoardPost.objects.filter(
            post_type=CommentBoardPost.PostType.GENERAL
        ).order_by('-id')
        context['job_openings'] = CommentBoardPost.objects.filter(
            post_type=CommentBoardPost.PostType.JOB_OPENING
        ).order_by('-id')
        context['public_classes'] = CommentBoardPost.objects.filter(
            post_type=CommentBoardPost.PostType.PUBLIC_CLASS
        ).order_by('-id')

        # Add the comment form
        context['comment_form'] = CommentForm()

        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'dancer_profile'):
                context['profile_image'] = self.request.user.dancer_profile.image
                context['profile_url'] = reverse('dancer_profile_detail', kwargs={'pk': self.request.user.dancer_profile.pk})
            elif hasattr(self.request.user, 'recruiter_profile'):
                context['profile_image'] = self.request.user.recruiter_profile.image
                context['profile_url'] = reverse('recruiter_profile_detail', kwargs={'pk': self.request.user.recruiter_profile.pk})


        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')  # Hidden input for post ID
            post = CommentBoardPost.objects.get(id=post_id)
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog_home')  # Replace 'blog_home' with the actual name of your blog home URL

        # Re-render the page with the form errors
        context = self.get_context_data(**kwargs)
        context['comment_form'] = form
        return self.render_to_response(context)
    

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        user = self.request.user
        profile_user = self.get_object().dancerUser

        # Fetch the dancer's posts
        context['dance_posts'] = DancePost.objects.filter(
            poster=profile.dancerUser
        ).order_by('-created_at')

        # Fetch comment board posts authored by this user's profile
        context['comment_board_posts'] = CommentBoardPost.objects.filter(
            author=profile.dancerUser
        ).order_by('-id')

        context['is_own_profile'] = profile.dancerUser == self.request.user
        context['is_friend'] = Friendship.objects.filter(user=user, friend=profile.dancerUser).exists()
        context['can_add_friend'] = user != profile.dancerUser and not context['is_friend']
        context['friends'] = Friendship.objects.filter(user=profile.dancerUser).select_related('friend')
        

        return context
   

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        user = self.request.user
        profile_user = self.get_object().recruiterUser

        # Fetch dance posts by this user's profile
        context['dance_posts'] = DancePost.objects.filter(
            poster=profile.recruiterUser
        ).order_by('-created_at')

        # Fetch comment board posts authored by this user's profile
        context['comment_board_posts'] = CommentBoardPost.objects.filter(
            author=profile.recruiterUser
        ).order_by('-id')

        # Add a flag for own profile
        context['is_own_profile'] = profile.recruiterUser == self.request.user
        context['is_friend'] = Friendship.objects.filter(user=user, friend=profile.recruiterUser).exists()
        context['can_add_friend'] = user != profile.recruiterUser and not context['is_friend']
        context['friends'] = Friendship.objects.filter(user=profile.recruiterUser).select_related('friend')


        return context


class SendMessageView(LoginRequiredMixin, FormView):
    template_name = 'project/send_message.html'
    form_class = PrivateMessageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receiver_id = self.kwargs['receiver_id']
        receiver = get_object_or_404(User, pk=receiver_id)

        # Determine the receiver's profile type
        if hasattr(receiver, 'dancer_profile'):
            context['receiver_profile_type'] = 'dancer'
            context['receiver_profile_pk'] = receiver.dancer_profile.pk
        elif hasattr(receiver, 'recruiter_profile'):
            context['receiver_profile_type'] = 'recruiter'
            context['receiver_profile_pk'] = receiver.recruiter_profile.pk

        context['receiver'] = receiver
        context['messages'] = PrivateMessage.objects.filter(
            Q(sender=self.request.user, receiver=receiver) |
            Q(sender=receiver, receiver=self.request.user)
        )

        return context

    def form_valid(self, form):
        receiver_id = self.kwargs['receiver_id']
        receiver = get_object_or_404(User, pk=receiver_id)

        # Save the new message
        form.instance.sender = self.request.user
        form.instance.receiver = receiver
        form.save()

        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path 


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
    template_name = 'project/create_dance_post.html'

    def form_valid(self, form):
        # Set the poster to the logged-in user
        form.instance.poster = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the appropriate profile
        if hasattr(self.request.user, 'dancer_profile'):
            return reverse('dancer_profile_detail', kwargs={'pk': self.request.user.dancer_profile.pk})
        elif hasattr(self.request.user, 'recruiter_profile'):
            return reverse('recruiter_profile_detail', kwargs={'pk': self.request.user.recruiter_profile.pk})
        return reverse('blog_home')

class CreateCommentBoardPostView(LoginRequiredMixin, CreateView):
    model = CommentBoardPost
    fields = ['content', 'post_type']
    template_name = 'project/create_comment_post.html'

    def form_valid(self, form):
        # Assign the logged-in user as the author
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog_home')  # Replace with the desired success redirect URL
    

class EditDancePostView(LoginRequiredMixin, UpdateView):
    model = DancePost
    fields = ['video', 'cut_music', 'description']
    template_name = 'project/edit_dance_post.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        # Check if the user is the author of the post
        if post.poster == request.user:
            # Redirect based on user type
            if hasattr(request.user, 'recruiter_profile'):
                return super().dispatch(request, *args, **kwargs)
            elif hasattr(request.user, 'dancer_profile'):
                return super().dispatch(request, *args, **kwargs)
        
        # If not the author, redirect to their respective profile
        if hasattr(request.user, 'recruiter_profile'):
            return redirect('recruiter_profile_detail', pk=request.user.recruiter_profile.pk)
        elif hasattr(request.user, 'dancer_profile'):
            return redirect('dancer_profile_detail', pk=request.user.dancer_profile.pk)
        
        # As a fallback, redirect to a safe default page
        return redirect('blog_home')

    def get_success_url(self):
        # Redirect to the appropriate profile page after editing
        if hasattr(self.request.user, 'recruiter_profile'):
            return reverse('recruiter_profile_detail', kwargs={'pk': self.request.user.recruiter_profile.pk})
        elif hasattr(self.request.user, 'dancer_profile'):
            return reverse('dancer_profile_detail', kwargs={'pk': self.request.user.dancer_profile.pk})
        return reverse('blog_home')  # Default fallback
    

class EditCommentBoardPostView(LoginRequiredMixin, UpdateView):
    model = CommentBoardPost
    fields = ['content', 'post_type']
    template_name = 'project/edit_comment_post.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        # Check if the user is the author of the post
        if post.author == request.user:
            # Redirect based on user type
            if hasattr(request.user, 'recruiter_profile'):
                return super().dispatch(request, *args, **kwargs)
            elif hasattr(request.user, 'dancer_profile'):
                return super().dispatch(request, *args, **kwargs)
        
        # If not the author, redirect to their respective profile
        if hasattr(request.user, 'recruiter_profile'):
            return redirect('recruiter_profile_detail', pk=request.user.recruiter_profile.pk)
        elif hasattr(request.user, 'dancer_profile'):
            return redirect('dancer_profile_detail', pk=request.user.dancer_profile.pk)
        
        # As a fallback, redirect to a safe default page
        return redirect('blog_home')

    def get_success_url(self):
        # Redirect to the appropriate profile page after editing
        if hasattr(self.request.user, 'recruiter_profile'):
            return reverse('recruiter_profile_detail', kwargs={'pk': self.request.user.recruiter_profile.pk})
        elif hasattr(self.request.user, 'dancer_profile'):
            return reverse('dancer_profile_detail', kwargs={'pk': self.request.user.dancer_profile.pk})
        return reverse('blog_home')  # Default fallback
    



def generate_graphs():
    # Data Preparation
    total_posts = DancePost.objects.count() + CommentBoardPost.objects.count()
    dance_posts_count = DancePost.objects.count()
    comment_posts_count = CommentBoardPost.objects.count()
    total_choreographers = RecruiterProfile.objects.count()
    total_dancers = DancerProfile.objects.count()

    posts_by_choreographers = DancePost.objects.filter(poster__recruiter_profile__isnull=False).count()
    posts_by_dancers = DancePost.objects.filter(poster__dancer_profile__isnull=False).count()

    # 1. Total Posts Pie Chart
    fig1, ax1 = plt.subplots()
    ax1.pie([dance_posts_count, comment_posts_count],
            labels=['Dance Posts', 'Comment Board Posts'],
            autopct='%1.1f%%',
            colors=['#ff9999', '#66b3ff'])
    ax1.set_title('Ratio of Post Types')

    buffer1 = BytesIO()
    plt.savefig(buffer1, format='png')
    buffer1.seek(0)
    image1_base64 = base64.b64encode(buffer1.getvalue()).decode()
    plt.close(fig1)

    # 2. Posts Distribution Bar Chart
    fig2, ax2 = plt.subplots()
    ax2.bar(['Choreographers', 'Dancers'], [posts_by_choreographers, posts_by_dancers], color=['#ffcc99', '#c2c2f0'])
    ax2.set_title('Posts by Choreographers vs Dancers')
    ax2.set_ylabel('Number of Posts')

    buffer2 = BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    image2_base64 = base64.b64encode(buffer2.getvalue()).decode()
    plt.close(fig2)

    return image1_base64, image2_base64

def graphs_page(request):
    image1_base64, image2_base64 = generate_graphs()

    return render(request, 'project/graphs_page.html', {
        'image1_base64': image1_base64,
        'image2_base64': image2_base64,
    })


class AddFriendView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        friend = get_object_or_404(User, id=user_id)

        # Prevent adding yourself as a friend
        if request.user == friend:
            return redirect('user_profile')

        # Create a friendship if it doesn't already exist
        Friendship.objects.get_or_create(user=request.user, friend=friend)
        Friendship.objects.get_or_create(user=friend, friend=request.user)

        # Redirect back to the friend's profile
        if hasattr(friend, 'dancer_profile'):
            return redirect('dancer_profile_detail', pk=friend.dancer_profile.pk)
        elif hasattr(friend, 'recruiter_profile'):
            return redirect('recruiter_profile_detail', pk=friend.recruiter_profile.pk)

        return redirect('user_profile')  # Fallback if no profile is found
    

class DeleteDancePostView(LoginRequiredMixin, DeleteView):
    model = DancePost
    def get_success_url(self):
        # Redirect to the appropriate profile page after editing
        if hasattr(self.request.user, 'recruiter_profile'):
            return reverse('recruiter_profile_detail', kwargs={'pk': self.request.user.recruiter_profile.pk})
        elif hasattr(self.request.user, 'dancer_profile'):
            return reverse('dancer_profile_detail', kwargs={'pk': self.request.user.dancer_profile.pk})
        return reverse('blog_home')  # Default fallback
    

    def get_queryset(self):
        # Ensure the logged-in user can only delete their own posts
        return super().get_queryset().filter(poster=self.request.user.dancer_profile)


class DeleteCommentPostView(LoginRequiredMixin, DeleteView):
    model = CommentBoardPost
    def get_success_url(self):
        # Redirect to the appropriate profile page after editing
        if hasattr(self.request.user, 'recruiter_profile'):
            return reverse('recruiter_profile_detail', kwargs={'pk': self.request.user.recruiter_profile.pk})
        elif hasattr(self.request.user, 'dancer_profile'):
            return reverse('dancer_profile_detail', kwargs={'pk': self.request.user.dancer_profile.pk})
        return reverse('blog_home')  # Default fallback
    def get_queryset(self):
        # Ensure the logged-in user can only delete their own posts
        return super().get_queryset().filter(author=self.request.user)
