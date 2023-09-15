from django.db import models
from .attendee import Attendee
from .event import Event

class EventAttendee(models.Model):

	attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
