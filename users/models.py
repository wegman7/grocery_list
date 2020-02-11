from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class List(models.Model):
    list_name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.list_name

class ListItem(models.Model):
    item = models.CharField(max_length=200)
    date_added = models.DateTimeField(default=timezone.now)
    from_list = models.ForeignKey(List, on_delete=models.CASCADE)

    def __str__(self):
        return self.item

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friend = models.ManyToManyField("Profile", blank=True)

    def __str__(self):
        return self.user.username

class FriendRequest(models.Model):
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('to_user', 'from_user')

    def __str__(self):
        return "From %s to %s" % (self.from_user.username, self.to_user.username)


# class List(models.Model):
#     item = models.CharField(max_length=200)
#     date_added = models.DateTimeField(default=timezone.now)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.item
