from django.db import models

# Create your models here.


class UserInfo(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    def __str__(self):
        return "%s" % self.pk


class UserSite(models.Model):
    receiver = models.CharField(max_length=50)
    site = models.CharField(max_length=200)
    zip = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    user = models.ForeignKey('UserInfo')
