import json
import requests
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
import secrets
from ybmenpilot.models import Participant 
from django.db import IntegrityError

user_authenticated = False

@csrf_exempt
def home(request):
	context = {}
	return render(request, 'home.html', context)
	#return render_to_response(request,'home.html')

@csrf_exempt
def get_access_token(request):
	req = request
	access_token = req.POST['access_token']
	user_id = req.POST['user_id']

	# handle errors

	response = requests.get('https://graph.facebook.com/oauth/access_token', params={'grant_type':'fb_exchange_token','client_id':'1446542485629653','client_secret':secrets.client_secret,'fb_exchange_token':access_token})
	# this is not json.
	#mtch = re.search(r"^=(\w*)&", response.text)
	firstbit = len("access_token=")
	lastind = response.text.find("&")
	mtch = response.text[firstbit:lastind]
	user_authenticated = True # flip auth flag

	# save info to database; need error checks for primary key
	try:
		# save identity and token
		Participant.objects.get_or_create(ident=user_id,token=mtch)
		# try to get and save other information?
	except IntegrityError: # except object already exists
	 	# update token if necessary
		p = Participant.objects.get(ident=user_id)
		p.token = mtch
		p.save()
	


	return HttpResponse("success authorized", content_type='text/plain') # return plain text to browser... probably shouldn't do that
	# handle response
	# save extended token to database

