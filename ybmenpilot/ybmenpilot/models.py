from django.db import models

class Update(models.Model):
	post_id = models.TextField(primary_key=True,max_length=100)
	content = models.TextField()
	link = models.CharField(max_length=200)
	date_posted = models.DateField()
	person_id = models.CharField(max_length=100)

class Participant(models.Model):
	ident = models.CharField(max_length=200)
	name = models.CharField(max_length=80,default="")
	token = models.CharField(max_length = 4000)
	birthday = models.CharField(max_length=12, default="")
	expirytoken = models.CharField(max_length=20,default="")
	num_likes = models.IntegerField(default=0)
	

class GroupPost(models.Model):
	ident = models.CharField(primary_key=True,max_length=100)
	content = models.TextField()
	date_posted = models.DateField()
	time_posted = models.CharField(max_length=25)
	num_comments_recd = models.IntegerField(default=0,editable=True)
	num_likes_recd = models.IntegerField(default=0)
	num_shares = models.IntegerField(default=0) # hm
	#people_liked = models.ListField() # list of participant ids

class GroupComment(models.Model):
	ident = models.CharField(primary_key=True,max_length=100)
	content = models.TextField()
	date_posted = models.DateField()
	time_posted = models.CharField(max_length=25)
	num_likes_recd = models.IntegerField()

