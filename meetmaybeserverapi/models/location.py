from django.db import models
from .location_type import LocationType
from .attendee import Attendee

class Location(models.Model):
  
  name = models.CharField(max_length=100)
  address = models.CharField(max_length=200)
  hours = models.CharField(max_length=200)
  attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
  location_type = models.ForeignKey(LocationType, on_delete=models.CASCADE)
