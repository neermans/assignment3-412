from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import * 
urlpatterns = [
    path('', BlogHomeView.as_view(), name='blog_home'), # landing page
    path('dancer_profile/<int:pk>/', DancerProfileDetailView.as_view(), name='dancer_profile_detail'), # dancer profile page
    path('create_dancer_profile/', CreateDancerProfileView.as_view(), name='create_dancer_profile'), # creating the dancer profile
    path('create_recruiter_profile/', CreateRecruiterProfileView.as_view(), name='create_recruiter_profile'), # creating recruiter profile
    path('recruiter_profile/<int:pk>/', RecruiterProfileDetailView.as_view(), name='recruiter_profile_detail'), # recruiter profile page
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'), # login page
    path('profiles/', ProfileListView.as_view(template_name='project/profile_list.html'), name='profile_list'), # list of profiles
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'), # logout page
    path('message/send/<int:receiver_id>/', SendMessageView.as_view(), name='send_message'), # sending message to another profile
    path('dancer_profile/edit/<int:pk>/', EditDancerProfileView.as_view(), name='edit_dancer_profile'), # editing the logged in profiles dance page
    path('recruiter_profile/edit/<int:pk>/', EditRecruiterProfileView.as_view(), name='edit_recruiter_profile'), # editing the logged in recruiters dance page
    path('dance_post/create/', CreateDancePostView.as_view(), name='create_dance_post'), # creating a dance post of either video or cut music
    path('comment_post/create/', CreateCommentBoardPostView.as_view(), name='create_comment_post'), # creating a comment post of one of the three topics
    path('dance_post/edit/<int:pk>/', EditDancePostView.as_view(), name='edit_dance_post'), # editing your profiles dance post
    path('comment_post/edit/<int:pk>/', EditCommentBoardPostView.as_view(), name='edit_comment_post'), # editing your profiles comment post
    path('graphs/', graphs_page, name='graphs_page'), # graphs page with different analytics
    path('add_friend/<int:user_id>/', AddFriendView.as_view(), name='add_friend'), # adding a friend

]
