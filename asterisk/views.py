# Create your views here.
import time, datetime
from django.contrib.auth.models import User
from hackerspace_management.asterisk.models import *
from django.shortcuts import render_to_response

def callback_add(request, authCode):
	try:
		u = User.objects.get(details__access_code = authCode)
		callback = CallBack(user=u, time=datetime.datetime.now())
		callback.save()
		retstr = "Calling Back: %s" % (callback.user.details.phone_number)
	except:
		retstr = "Authentication Error"

	timestamp = "Time: %s" % (datetime.datetime.now())
	return render_to_response('callback_add.html', {'response': retstr, 'timestamp': timestamp})
