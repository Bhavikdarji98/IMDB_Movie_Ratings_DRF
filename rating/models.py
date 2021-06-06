from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group


# Create your models here.

class MovieRatings(models.Model):
    """
    This model will store the
    movie rating information from https://www.imdb.com/chart/top?ref_=nv_mv_250
    to access the data via APIs
    """
    name = models.CharField(max_length= 100, blank= True, null= True)
    rating = models.FloatField(blank= True, null= True)
    release_date = models.DateTimeField(blank= True, null= True, max_length=50)
    duration = models.CharField(blank= True, null= True, max_length= 10)
    description = models.TextField(max_length= 500, blank= True, null= True)

    def __str__(self):
        return self.name

phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be entered in the format: 9999999999")

class User(AbstractUser):
    email = models.EmailField(unique=True, help_text='This field is required.')
    mobile_number = models.CharField(max_length=10, unique=True, validators=[phone_regex], blank=True, null=True)
    jwt_secret = models.CharField(blank=True, null=True, max_length=500)

    def __str__(self):
        return self.email