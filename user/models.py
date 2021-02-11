from django.db import models
from django.contrib.auth.models import AbstractUser
from user.managers import CustomUserManager
# Create your models here.

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('None', 'Prefer not to say'),
]


class User(AbstractUser):
    picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    full_name = models.CharField(max_length=100,help_text='Help people discover your account by using the name you\'re known by: either your full name, nickname, or business name.')
    email = models.EmailField(unique=True)

    # extra not required fields
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    is_account_private = models.BooleanField(default=False)
    website = models.URLField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True, help_text='Provide your personal information, even if the account is used for a business, a pet or something else. This won\'t be a part of your public profile.')

    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','username',]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def posts_count(self):
        count = self.post_set.count()
        return count

    @property
    def followers_count(self):
        count = self.follow_user.filter(is_follow=True).count()
        return count

    @property
    def followings_count(self):
        count = self.follow_follower.filter(is_follow=True).count()
        return count