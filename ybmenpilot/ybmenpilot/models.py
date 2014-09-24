from django.db import models

class Update(models.Model):
	post_id = models.CharField(primary_key=True,max_length=100)
	content = models.TextField(default="")
	date_posted =  models.TextField(max_length=100,default="")
	time_posted = models.CharField(max_length=25,default="")
	link = models.CharField(max_length=200,default="")
	person_id = models.CharField(max_length=100)
	content_type = models.CharField(max_length=25)
	imagecontent = models.CharField(max_length=1000)
	num_comments_recd = models.IntegerField(default=0)
	num_likes_recd = models.IntegerField(default=0)
	addl_content = models.TextField(default="")
	application = models.CharField(max_length=200,default="")

class Participant(models.Model):
	ident = models.CharField(primary_key=True,max_length=200)
	name = models.CharField(max_length=80,default="")
	token = models.CharField(max_length = 4000)
	#birthday = models.CharField(max_length=12, default="") # how are we getting this info, bday or age range
	age_min = models.IntegerField(default=0)
	expirytoken = models.CharField(max_length=20,default="")
	num_likes = models.IntegerField(default=0)
	gender = models.CharField(max_length=20,default="")
	hometown = models.CharField(max_length=100,default="")
	group_admin = models.BooleanField(default=False)


class GroupPost(models.Model):
	ident = models.CharField(primary_key=True,max_length=100)
	content = models.TextField(default="")
	date_posted = models.CharField(max_length=25,default="")#models.DateField()
	time_posted = models.CharField(max_length=25,default="")
	num_comments_recd = models.IntegerField(default=0,editable=True)
	num_likes_recd = models.IntegerField(default=0)
	num_shares = models.IntegerField(default=0) # hm
	link = models.CharField(max_length=100,default="")
	imagecontent = models.CharField(max_length=1000,default="")
	#people_liked = models.ListField() # list of participant ids

class GroupComment(models.Model):
	ident = models.CharField(primary_key=True,max_length=100)
	content = models.TextField()
	date_posted = models.DateField()
	time_posted = models.CharField(max_length=25)
	num_likes_recd = models.IntegerField()
	poster = models.CharField(max_length=100,default="") # user id of commenter - anon schema

