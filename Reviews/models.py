from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from Authentication.models import CustomUser
from django.core.validators import MinValueValidator,MaxValueValidator


class Review(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    bootcamp = models.ForeignKey('Bootcamps.Bootcamp', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 


    def get_average_rating(self):
        avg_rating = Review.objects.filter(bootcamp_id=self.bootcamp_id).aggregate(models.Avg('rating'))['rating__avg']
        if avg_rating is not None:
            bootcamp = Review.objects.get(id=self.bootcamp_id)
            bootcamp.average_rating = round(avg_rating, 1)
            bootcamp.save()
        else:
            self.bootcamp.average_rating = None
            self.bootcamp.save()



@receiver(post_save, sender=Review)
def update_average_rating_on_review_save(sender, instance, **kwargs):
       instance.get_average_rating()

@receiver(post_delete, sender=Review)
def update_average_rating_on_review_delete(sender, instance, **kwargs):
      instance.get_average_rating()