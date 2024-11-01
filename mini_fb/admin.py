#mini_fb/admin
# tell the admin we want to administer these models
from django.contrib import admin
from .models import Profile
# Register your models here.


from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name','last_name')
    search_fields = ('user__username', 'first_name', 'last_name')

admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(Friend)