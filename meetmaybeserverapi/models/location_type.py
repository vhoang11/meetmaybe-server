from django.db import models

class LocationType(models.Model):
  
  label = models.CharField(max_length=55)
  dress_code = models.CharField(max_length=100)
