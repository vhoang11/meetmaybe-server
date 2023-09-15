from django.db import models

class Attendee(models.Model):
		
		name = models.CharField(max_length=200)
		username = models.CharField(max_length=200)
		email = models.CharField(max_length=200)
		profile_image_url = models.CharField(max_length=1000)
		bio = models.CharField(max_length=500)
		uid = models.CharField(max_length=100)
