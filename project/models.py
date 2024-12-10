from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class DancerProfile(models.Model):
    dancerUser = models.OneToOneField(User, on_delete=models.CASCADE,related_name="dancer_profile")
    name = models.CharField(max_length=100)
    preferred_styles = models.ManyToManyField('DanceStyle')
    bio = models.TextField()
    job_history = models.TextField()
    image = models.URLField(max_length=200, blank = True, null=True)


    def __str__(self):
        return f"{self.name} 's Profile"


class RecruiterProfile(models.Model):
    name = models.CharField(max_length=100)
    recruiterUser = models.OneToOneField(User, on_delete=models.CASCADE)
    dance_company = models.CharField(max_length=255)
    email_contact = models.EmailField()
    image = models.URLField(max_length=200, blank=True, null=True)


    def __str__(self):
        return f"{self.name} - {self.dance_company}'s profile"
    


class DanceStyle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    


class DancePost(models.Model):
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    cut_music = models.FileField(upload_to='music/', blank=True, null=True)
    description = models.TextField()
    poster = models.ForeignKey(DancerProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.video:
            return f"Video Post by {self.poster.name}"
        elif self.cut_music:
            return f"Music Post by {self.poster.name}"
        else:
            return f"Post by {self.poster.name}"
        

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} "


class CommentBoardPost(models.Model):
    class PostType(models.TextChoices):
        JOB_OPENING = 'JO', 'Job Opening'
        PUBLIC_CLASS = 'PC', 'Public Class'
        GENERAL = 'GE', 'General'

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    post_type = models.CharField(
        max_length=2,
        choices=PostType.choices,
        default=PostType.GENERAL
    )

    def __str__(self):
        return f"{self.get_post_type_display()} by {self.author} "
