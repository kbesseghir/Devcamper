from django.db import models
from Authentication.models import *

from django.db import models
from django.utils.text import slugify
from geopy.geocoders import Nominatim  # You can use a geocoding library like geopy

class Bootcamp(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(max_length=500)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255)
    
    # Location
    coordinates = models.PointField(geography=True, blank=True, null=True)
    formatted_address = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Other fields
    careers = models.ManyToManyField('Career', related_name='bootcamps')
    average_rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True)
    average_cost = models.FloatField(blank=True, null=True)
    photo = models.ImageField(upload_to='bootcamps/', default='no-photo.jpg')
    housing = models.BooleanField(default=False)
    job_assistance = models.BooleanField(default=False)
    job_guarantee = models.BooleanField(default=False)
    accept_gi = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'Bootcamps'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.address:
            geolocator = Nominatim(user_agent='your_app_name')
            location = geolocator.geocode(self.address)
            if location:
                self.coordinates = f'POINT({location.longitude} {location.latitude})'
                self.formatted_address = location.address
                self.street = location.raw.get('address', {}).get('road', '')
                self.city = location.raw.get('address', {}).get('city', '')
                self.state = location.raw.get('address', {}).get('state', '')
                self.zipcode = location.raw.get('address', {}).get('postcode', '')
                self.country = location.raw.get('address', {}).get('country', '')
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        Course.objects.filter(bootcamp=self).delete()
        Review.objects.filter(bootcamp=self).delete()
        super().delete(*args, **kwargs)

class Career(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Course(models.Model):
    bootcamp = models.ForeignKey(Bootcamp, on_delete=models.CASCADE, related_name='courses')
    # Define other course fields

class Review(models.Model):
    bootcamp = models.ForeignKey(Bootcamp, on_delete=models.CASCADE, related_name='reviews')
    # Define other review fields

class User(models.Model):
    # Define user fields
