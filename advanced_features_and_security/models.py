from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, date_of_birth=None, profile_photo=None):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            profile_photo=profile_photo,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, date_of_birth=None, profile_photo=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            date_of_birth=date_of_birth,
            profile_photo=profile_photo,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    date_of_birth=models.DateField(blank=True, null=True)
    profile_photo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f"{self.username}: {self.email}, {self.date_of_birth}"

class Author(models.Model):
    name = models.CharField(max_lenght=20)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        permissions = [
            ('can_view_book', 'Can view book'),
            ('can_create_book', 'Can create book'),
            ('can_edit_book', 'Can edit book'),
            ('can_delete_book', 'Can delete book'),
        ]

    name = models.CharField(("name")), max_length=150, unique=True
    permissions = models.ManyToManyField(
        permissions,
        verbose_name=("permissions"),
        blank=True,
    )

    class UserGroup(Group):
        ...

        def __str__(self):
            return f"{self.name}: {self.permissions}"