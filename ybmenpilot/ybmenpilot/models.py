from django.db import models

class Updates(models.Model):
	post_id = models.TextField(primary_key=True,max_length=100)
	content = models.TextField()
	link = models.CharField(max_length=200)
	date_posted = models.DateField()
	person_id = modesl.CharField(max_length=100)

class Participant(models.Model):
	