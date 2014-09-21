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
	# error checks
	#assert access_token 
	#assert len(access_token) < 4000
	#if not accesstoke
	# exchange token for extended token now
	response = requests.get('https:/graph.facebook.com/oauth/access_token', params={'grant_type':'fb_exchange_token','client_id':'1446542485629653','client_secret':secrets.client_secret,'fb_exchange_token':access_token})
	resp = json.loads(response.text)
	#context = {'resp':str(resp)}
	#return Http(str(resp))

	# handle response
	# save extended token to database

