from django.db import models
from django.contrib import auth

class User(auth.models.User, auth.models.PermissionsMixin):

        def __Str__(self):
            return "@{}".format(self.username)

# Create your models here.
