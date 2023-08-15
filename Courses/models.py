from django.db import models
from Bootcamps.models import *
from Authentication.models import *

class Course(models.Model):


    from django.core.validators import MinValueValidator

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    weeks = models.CharField(max_length=20)
    tuition = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    minimum_skill = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'), 
        ('advanced', 'Advanced')
          ])
    scholarship_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    bootcamp = models.ForeignKey(Bootcamp, on_delete=models.CASCADE, related_name='courses')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Courses'
        
    