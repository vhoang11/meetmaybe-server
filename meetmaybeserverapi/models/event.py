from django.db import models
from .attendee import Attendee

class Event(models.Model):

	title = models.CharField(max_length=100)
	image_url = models.CharField(max_length=1000)
	description = models.CharField(max_length=1000)
	location = models.CharField(max_length=1000)
	date = models.DateField()
	time = models.TimeField()
	organizer = models.ForeignKey(Attendee, on_delete=models.CASCADE)
	invitee = models.ForeignKey(Attendee, on_delete=models.CASCADE, related_name='invitee')
	is_public = models.BooleanField()
	organizer_canceled = models.BooleanField()
	invitee_canceled = models.BooleanField()
 
	@property
	def joined(self):
		return self._joined

	@joined.setter
	def joined(self, value):
		self._joined = value
