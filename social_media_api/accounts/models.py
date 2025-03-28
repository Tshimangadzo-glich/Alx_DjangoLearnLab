from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username cannot be empty!')
        user = self.model(username=username, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)       

class CustomUser(AbstractUser):
    bio = models.TextField()
    profile_photo = models.ImageField(upload_to='profile_pictures')
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')

    objects = CustomUserManager()
    REQUIRED_FIELDS = ['bio', 'profile_photo', 'followers']