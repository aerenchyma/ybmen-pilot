import json
import requests
import secrets # for keeping app secret
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from ybmenpilot.models import Participant 
from django.db import IntegrityError

user_authenticated = False

# user stuff --
# no, could do this in the task for all authenticated users

## views

@csrf_exempt
def home(request):
	context = {}
	# potential check in tpl later for user_authenticated?
	return render(request, 'home.html', context)
	#return render_to_response(request,'home.html')

@csrf_exempt
def get_access_token(request):
	req = request
	access_token = req.POST['access_token']
	user_id = req.POST['user_id']

	# handle errors
	assert access_token
	assert len(access_token) < 6000

	response = requests.get('https://graph.facebook.com/oauth/access_token', params={'grant_type':'fb_exchange_token','client_id':'1446542485629653','client_secret':secrets.client_secret,'fb_exchange_token':access_token})
	# this response is not json.

	# vaguely silly way of parsing the not-json response that should work anyway
	firstbit = len("access_token=")
	lastind = response.text.find("&")
	mtch = response.text[firstbit:lastind]
	user_authenticated = True # flip auth flag (if needed for tpl)

	# save necessary info to database; need error checks for primary key
	try:
		# save identity and token
		p,created = Participant.objects.get_or_create(ident=user_id,token=mtch)
		# try to get and save other information?
	except IntegrityError: # except object already exists
	 	# update token if necessary
	 	#std.out.write("excepted")
		p = Participant.objects.filter(ident=user_id)
		if len(p) == 1:
			p = p[0]
			p.token = mtch
			p.save()
	
	return HttpResponse("success authorized", content_type='text/plain') # return plain text to browser... probably shouldn't do that
	# handle response
	# save extended token to database

