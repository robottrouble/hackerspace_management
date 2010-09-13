from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserDetails(models.Model):
	asterisk_extension = models.CharField(max_length=4)
	access_code = models.CharField(max_length=4)
	access_message = models.CharField(max_length=2048)
	phone_number = models.CharField(max_length=10)
	user = models.OneToOneField(User, related_name="details")

	def __unicode__(self):
		return self.user.username

class CallBack(models.Model):
	user = models.ForeignKey(User, related_name="calls")
	time = models.DateTimeField()
	returned = models.BooleanField(default=False)

	def __unicode__(self):
		retstr = "User: %d Time: %s Returned: %s" % (self.user.id, self.time, self.returned)
		return retstr

class FailedAuth(models.Model):
	method = models.CharField(max_length=4)
	data = models.CharField(max_length=4)
	time = models.DateTimeField()

	def assign(self, user):
		if self.method == 'AST':
			user.details.access_code = self.data
		elif self.method == 'SMS':
			user.details.access_message = self.data
		user.details.save()

	def __unicode__(self):
		retstr = "ID: %d Time: %s Data: %s" % (self.id, self.time, self.data)
		return retstr
