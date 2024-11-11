# mini_fb/models.py
# define the data objects for our application

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User # import the User model

# Profile Model
class Profile(models.Model):

    # every Article has one User:
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #data attributes of a profile
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    email = models.EmailField()
    profile_image_url = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # Method to get all status messages for the profile
    def get_status_messages(self):
        return self.statusmessage_set.all().order_by('-timestamp')
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_status_messages(self):
        return self.statusmessage_set.order_by('-timestamp')  # Retrieve status messages by timestamp
    
    def get_friends(self):
        # get friends depending on whether this profile is profile1 or profile2
        friends_profile1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends_profile2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)

        # Combine both lists and retrieve Profile objects
        friend_ids = list(friends_profile1) + list(friends_profile2)
        return Profile.objects.filter(id__in=friend_ids).distinct()
    
    def add_friend(self, other):
        # Making sure the user cannot add themselves as a friend
        if self == other:
            raise ValueError("Cannot befriend oneself.")

        # Checking if the friendship already exists in either direction
        existing_friendship = Friend.objects.filter(
            models.Q(profile1=self, profile2=other) | 
            models.Q(profile1=other, profile2=self)
        ).exists()

        if not existing_friendship:
            # Create new friendship if it does not exists
            Friend.objects.create(profile1=self, profile2=other, timestamp=timezone.now())
        else:
            # Handle the case where the friendship already exists
            print("Friendship already exists.")

    def get_friend_suggestions(self):
        # Returns a QuerySet of profile suggestions for new friends.
        current_friends = self.get_friends()
        all_profiles = Profile.objects.exclude(id=self.id)  # Exclude the current profile
        # Exclude all current friends from the suggestions
        suggestions = all_profiles.exclude(id__in=current_friends.values_list('id', flat=True))
        return suggestions
    
    def get_news_feed(self):
        # Returns a QuerySet of all status messages for the profile and the profile's friends.# 
        # Get friend profiles
        friends = self.get_friends()
        
        # Get status messages for this profile and for each friend
        news_feed = StatusMessage.objects.filter(
            Q(profile=self) | Q(profile__in=friends)
        ).order_by('-timestamp')  # Most recent first

        return news_feed


# StatusMessage Model
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        # Display the first 30 characters of the message in the admin panel
        return f"Message from {self.profile.first_name}: {self.message[:30]}..."
    
    def get_images(self):
        # Return all related images for this StatusMessage
        images = Image.objects.filter(status_message=self)
        return images

# Image Model
class Image(models.Model):
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # Display the idea of an image 
        return f"Image for {self.image} uploaded at {self.uploaded_at}"
    

# Friend model
class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friends_profile1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friends_profile2")
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profile1} & {self.profile2}"
    
