from django.contrib import admin
from .models import List, ListItem, Profile, FriendRequest

admin.site.register(List)
admin.site.register(ListItem)
admin.site.register(Profile)
admin.site.register(FriendRequest)