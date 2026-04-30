from django.db import models

# Create your models here.
class Accounts(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=190)
    password = models.CharField(max_length=140)
    confirm_password = models.CharField(max_length=140)

    def __str__(self):
        return f"Hi {self.username}, your account has been created successflly"
    