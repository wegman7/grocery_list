from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class List(models.Model):
    item = models.CharField(max_length=200)
    date_added = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.item

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friend = models.ManyToManyField("Profile", blank=True)

    def __str__(self):
        return self.user.username

# might be better to recieve friend requests from users instead of profiles
class FriendRequest(models.Model):
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('to_user', 'from_user')

    def __str__(self):
        return "From %s to %s" % (self.from_user.username, self.to_user.username)