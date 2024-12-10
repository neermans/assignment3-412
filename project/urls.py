from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import * 

urlpatterns = [
    path('', BlogHomeView.as_view(), name='blog_home'),
    path('dancer_profile/<int:pk>/', DancerProfileDetailView.as_view(), name='dancer_profile_detail'),
    path('create_dancer_profile/', CreateDancerProfileView.as_view(), name='create_dancer_profile'),
    path('create_recruiter_profile/', CreateRecruiterProfileView.as_view(), name='create_recruiter_profile'),
    path('recruiter_profile/<int:pk>/', RecruiterProfileDetailView.as_view(), name='recruiter_profile_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('profiles/', ProfileListView.as_view(template_name='project/profile_list.html'), name='profile_list'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'), 
    path('message/send/<int:receiver_id>/', SendMessageView.as_view(), name='send_message'),
    path('dancer_profile/edit/<int:pk>/', views.EditDancerProfileView.as_view(), name='edit_dancer_profile'),
    path('recruiter_profile/edit/<int:pk>/', views.EditRecruiterProfileView.as_view(), name='edit_recruiter_profile'),
    path('dance_post/create/', CreateDancePostView.as_view(), name='create_dance_post'),
    path('comment_post/create/', CreateCommentBoardPostView.as_view(), name='create_comment_post'),






]

#path('', BlogHomeView.as_view(), name='blog_home'),
#    path('login/', LoginView.as_view(), name='login'),
#    path('register/dancer/', CreateDancerProfileView.as_view(), name='register_dancer'),
#    path('register/recruiter/', CreateRecruiterProfileView.as_view(), name='register_recruiter'),
#    path('profiles/', ProfileListView.as_view(), name='profile_list'),
#    path('dashboard/', DashboardView.as_view(), name='dashboard'),
#    path('post/new/', CreatePostView.as_view(), name='create_post'),
#    path('messages/', MessageListView.as_view(), name='messages'),
#    path('messages/new/', CreateMessageView.as_view(), name='create_message'),