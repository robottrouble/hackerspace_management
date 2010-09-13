from django.db import models
from django import template 
from django.contrib.auth.models import User
import locale, os

locale.setlocale(locale.LC_ALL, '')

# Create your models here.

class Parts(models.Model):
	name = models.CharField(max_length=128)
	description = models.CharField(max_length = 1024)
	minimum_stock = models.PositiveIntegerField(default = 0)
	cross_reference = models.ManyToManyField("self")
        photo = models.ImageField(upload_to='images/parts_photos', blank=True, null=True)
        thumbnail = models.ImageField(upload_to='images/parts_thumbnails', blank=True, null=True, editable=False)
        created_by = models.ForeignKey(User, null=False, blank=False, related_name='created_parts')
        modified_by =  models.ForeignKey(User, null=False, blank=False, related_name='modified_parts')
	TYPE_CHOICES = (
		('P', 'Part'),
		('T', 'Tool')
	)
	type = models.CharField(max_length = 1, null=False, blank=False, choices=TYPE_CHOICES)

	def __unicode__(self):
                return self.name

        def get_reorder_count(self):
                return self.minimum_stock - self.stock.count()

        def get_reorder_items(self):
                # FIXME - There's gotta be a better way...
                p = Parts.objects.filter(minimum_stock__gt=0)

                for part in p:
                        if part.stock.select_related().count() >= part.minimum_stock:
                                print part
                                p = p.exclude(pk=part.id)
                return p

	class Admin:
		pass

class PartAttachments(models.Model):
        part = models.ForeignKey(Parts, related_name="attachments", null=False)
        file = models.FileField(upload_to='attachments/part_attachments/', null=False)
        preview = models.ImageField(upload_to='attachments/part_attachments/previews', null=True, blank=True)

        def get_preview(self):
                return self.file

        def basename(self):
                return os.path.basename(self.file.name)

class Locations(models.Model):
	name = models.CharField(max_length = 128, unique=True)
	description = models.CharField(max_length = 1024)

	def __unicode__(self):
                return self.name

class Stock(models.Model):
	type = models.ForeignKey(Parts, related_name="stock")
        location = models.ForeignKey(Locations, related_name="stock")
        serial_number = models.CharField(max_length = 128, blank=True)
        def __unicode__(self):
                return self.type.name

class PartComponents(models.Model):
	parent_part = models.ForeignKey(Parts, related_name="components")
	child_part = models.ForeignKey(Parts, related_name="parent_parts")
	quantity = models.PositiveIntegerField(default = 1)

	def __str__(self):
	        return self.child_part.type.name

class Vendors(models.Model):
	name = models.CharField(max_length = 128, unique=True)
	URL = models.CharField(max_length = 1024, blank=True)
	phone = models.CharField(max_length = 10, blank=True)
	fax = models.CharField(max_length = 10, blank=True)

        def __str__(self):
                return self.name

class PartVendors(models.Model):
	part = models.ForeignKey(Parts,related_name='vendors')
	vendor= models.ForeignKey(Vendors,related_name='parts')
        part_number = models.CharField(max_length=2048, blank=True)
	URL = models.CharField(max_length=2048, blank=True)
	cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	minimum_order = models.PositiveIntegerField(default = 1, null=True)
       
        def cost_as_currency(self):
                locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
                costAsCurrency = locale.currency(self.cost)
                return costAsCurrency
        
        def __str__(self):
                return self.part.name + " - " + self.vendor.name

# class Users(models.Model):
#	user_name = models.CharField(max_length = 20)
#	real_name = models.CharField(max_length = 128)
#	email = models.CharField(max_length = 128)

class Comments(models.Model):
        part = models.ForeignKey(Parts, related_name='comments', null=True,blank=True)
        stock_item = models.ForeignKey(Stock, related_name='comments',null=True,blank=True)
        text = models.CharField(max_length = 1024) 
        author = models.ForeignKey(User)
        date = models.DateTimeField(auto_now_add=True)
