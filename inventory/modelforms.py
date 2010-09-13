from hackerspace_management.inventory.models import *
from django.forms import ModelForm

class PartsForm(ModelForm):
        class Meta:
                model = Parts
                exclude = ('cross_reference','created_by','modified_by')

class PartAttachmentsForm(ModelForm):
        class Meta:
                model = PartAttachments

class StockForm(ModelForm):
        class Meta:
                model = Stock

class LocationsForm(ModelForm):
        class Meta:
                model = Locations

class VendorsForm(ModelForm):
        class Meta:
                model = Vendors

class PartVendorsForm(ModelForm):
        class Meta:
                model = PartVendors
