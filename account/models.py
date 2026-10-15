from django.db import models

# Create your models here.
class Accounts(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=190)
    password = models.CharField(max_length=140)
    confirm_password = models.CharField(max_length=140)

    def __str__(self):
        return f"Hi {self.username}, your account has been created successflly"
    

class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    headline = models.CharField(max_length=160, blank=True)
    location = models.CharField(max_length=120, blank=True)
    bio = models.TextField(max_length=2000, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='followers')

    def __str__(self):
        return self.user.username
