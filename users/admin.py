from django.contrib import admin
from .models import List, Profile, FriendRequest

admin.site.register(List)
admin.site.register(Profile)
admin.site.register(FriendRequest)