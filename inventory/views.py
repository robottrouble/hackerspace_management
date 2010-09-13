# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from hackerspace_management.inventory.models import *
from hackerspace_management.inventory.modelforms import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth import logout
from django.template import RequestContext
from django.core.files.base import ContentFile
from django.conf import settings

def default(request):
        return render_to_response('default.html', {})

# PARTS
def parts_view_all(request):
        parts_list = Parts.objects.all()
        if request.POST:
                if request.POST["Submit"] == "Search":
                        partSearch = request.POST["txtMasterPartSearch"]
                        parts_list = parts_list.filter(name__icontains=partSearch)

        paginator = Paginator(parts_list, 10)

        try:
                page = int(request.GET.get('page', '1'))
        except ValueError:
                page = 1

        try:
                parts = paginator.page(page)
        except (EmptyPage, InvalidPage):
                parts = paginator.page(paginator.num_pages)
        return render_to_response('parts_view_all.html', {'parts': parts}, context_instance=RequestContext(request))

def parts_components_edit(request, partTypeID):
        part = Parts.objects.get(pk=partTypeID)
        parts_list = None 
        if request.POST:
                if request.POST["Submit"] == "Search":
                        partSearch = request.POST["txtPartSearch"]
                        parts_list = Parts.objects.filter(name__icontains=partSearch).exclude(parent_parts__parent_part = part).exclude(id=part.id)

        if parts_list is None:
                parts_list = Parts.objects.exclude(parent_parts__parent_part = part).exclude(id=part.id)

        if request.POST:
                if request.POST["Submit"]:
                        if request.POST['Submit'] == 'Add':
                                childID = request.POST['add_part']
                                quantity = request.POST['quantity']
                                child = Parts.objects.get(pk=childID)
                                pc = PartComponents.objects.filter(parent_part=part, child_part=child).count()
                                if pc:
                                        print "HAS ONE!"
                                else:
                                        pc = PartComponents(parent_part=part, child_part=child, quantity=quantity)
                                        pc.save()
                        if request.POST['Submit'] == 'Remove':
                                childID = request.POST['update_part']
                                child = Parts.objects.get(pk=childID)
                                pc = PartComponents.objects.filter(parent_part=part, child_part=child).delete()

                        if request.POST['Submit'] == 'Update':
                                childID = request.POST['update_part']
                                quantity = request.POST['quantity']
                                child = Parts.objects.get(pk=childID)
                                pc = PartComponents.objects.filter(parent_part=part, child_part=child).update(quantity=quantity)

        paginator = Paginator(parts_list, 10)
        try:
                page = int(request.GET.get('page', '1'))
        except ValueError:
                page = 1

        try:
                parts = paginator.page(page)
        except (EmptyPage, InvalidPage):
                parts = paginator.page(paginator.num_pages)
        return render_to_response('parts_components_edit.html', {'part': part, 'parts': parts}, context_instance=RequestContext(request))

def parts_view(request, partTypeID):
        locale.setlocale(locale.LC_ALL, '')
        part = Parts.objects.get(pk=partTypeID) 
        if request.POST:
                if request.POST["Submit"] == "Add Comment":
                        user = User.objects.get(pk=1)
                        newComment = Comments(part=part, text=request.POST["text"], author=user).save()
                elif request.POST["Submit"] == "Add Attachment":
                        newPartAttachmentsForm = PartAttachmentsForm(request.POST, request.FILES)
                        print "saving...."
                        if newPartAttachmentsForm.is_valid():
                                newPartAttachmentsForm.save()
                                print "saved."
                        print newPartAttachmentsForm.errors
                        # file_content = ContentFile(request.FILES['file'].read())
                        # PartAttachments.file.save(request.FILES['file'].name, file_content)

                elif request.POST["Submit"] == "Add Vendor":
                        partVendorsForm = PartVendorsForm(data=request.POST)
                        if partVendorsForm.is_valid():
                                try:
                                        newPartVendor = partVendorsForm.save()
                                except:
                                        pass
                else:
                        form = StockForm(data=request.POST)
                        newPartLocation = Locations.objects.get(pk=request.POST['location'])
                        Stock(type=part, location=newPartLocation).save()

        stock = [ ]
        for location in Locations.objects.filter(stock__type=part).distinct():
                stock.append({'name': location.name, 'value': part.stock.filter(location=location).count()})

        stockForm = StockForm()
        partVendorsForm = PartVendorsForm()
        partAttachmentsForm = PartAttachmentsForm(instance=part)
        return render_to_response('parts_view.html',{'part': part,'stock': stock, 'stockForm': stockForm, 'partVendorsForm': partVendorsForm, 'partAttachmentsForm': partAttachmentsForm}, context_instance=RequestContext(request))
        
def parts_edit(request, partID):
        part = Parts.objects.get(pk=partID)
        if request.POST:
                if request.POST['Submit'] == 'Submit':
                        form = PartsForm(request.POST, request.FILES, instance=part)
                        if form.is_valid():
                                form.save()
                                return HttpResponseRedirect('/parts/view/%d/' % part.id)
                else:
                        return HttpResponseRedirect('/parts/view/%d/' % part.id)

        else:
                form = PartsForm(instance=part) 

        return render_to_response('parts_edit.html',{'part': part, 'form': form}, context_instance=RequestContext(request))

def parts_add(request):
        if request.POST:
                form = PartsForm(data=request.POST)
                if form.is_valid():
                        try:
                                newPart = form.save()
                        except:
                                pass
                        return HttpResponseRedirect('/parts/view/%d/' % newPart.id)
        else:
                form = PartsForm()

        return render_to_response('parts_add.html',{'form': form}, context_instance=RequestContext(request))
# VENDORS

def vendors_view_all(request):
        vendors_list = Vendors.objects.all()
        paginator = Paginator(vendors_list, 10)

        try:
                page = int(request.GET.get('page', '1'))
        except ValueError:
                page = 1

        try:
                vendors = paginator.page(page)
        except (EmptyPage, InvalidPage):
                vendors = paginator.page(paginator.num_pages)

        return render_to_response('vendors_view_all.html', {'vendors': vendors}, context_instance=RequestContext(request))

def vendors_view(request, vendorID):
        vendor = Vendors.objects.get(pk=vendorID)
        return render_to_response('vendors_view.html', {'vendor': vendor}, context_instance=RequestContext(request))

def vendors_add_edit(request, vendorID=None):
        if vendorID:
                vendor = Vendors.objects.get(pk=vendorID)
        else:
                vendor = Vendor()

        if request.POST:
                form = VendorsForm(data=request.POST, instance=vendor)
                if form.is_valid():
                        try:
                                newVendor = form.save()
                        except:
                                pass

                        if newVendor:
                                return HttpResponseRedirect('/vendors/view/%d/' % newVendor.id)
        else:
                form = VendorsForm(instance=vendor)
                
        return render_to_response('vendors_add_edit.html',{'form': form}, context_instance=RequestContext(request))        

def vendors_edit(request):
        return HttpResponse('Not Implemented')

def stock_view_all(request):
        stock_list = Stock.objects.all()
        if request.POST:
                if request.POST["txtPartSearch"]:
                        partTxt = request.POST["txtPartSearch"]
                        stock_list = stock_list.filter(type__name__icontains=partTxt)
                if request.POST["txtLocationSearch"]:
                        locTxt = request.POST["txtLocationSearch"]
                        stock_list = stock_list.filter(location__name__icontains=locTxt)
                         
        paginator = Paginator(stock_list, 10)
        try:
                page = int(request.GET.get('page', '1'))
        except ValueError:
                page = 1

        try:
                stock = paginator.page(page)
        except (EmptyPage, InvalidPage):
                stock = paginator.page(paginator.num_pages)

        return render_to_response('stock_view_all.html', {'stock': stock}, context_instance=RequestContext(request))

def stock_view(request, stockID):
        item = Stock.objects.get(pk=stockID)
        if request.POST:
                if request.POST["Submit_Comment"]:
                        user = User.objects.get(pk=1)
                        newComment = Comments(stock_item=item, text=request.POST["text"], author=user).save()
        part = item.type
        comments = item.comments.select_related()
        return render_to_response('stock_view.html', {'item': item, 'part': part, 'comments': comments}, context_instance=RequestContext(request))

@login_required
def stock_add_edit(request, itemID=None):
        if itemID:
                item = Stock.objects.get(pk=itemID)
        else:
                item = Stock()

        if request.POST:
                form = StockForm(data=request.POST, instance=item)
                if form.is_valid():
                        try:
                                quantity = int(request.POST['quantity'])
                                if quantity > 1:
                                        for i in range(quantity): 
                                                newStock = form.save()
                                                form = StockForm(data=request.POST)
                                else:
                                        newStock = form.save()
                        except:
                                pass

                        if newStock:
                                return HttpResponseRedirect('/stock/view/%d/' % newStock.id) 
        else:
                form = StockForm(instance=item)

        return render_to_response('stock_add.html',{'form': form}, context_instance=RequestContext(request))

def parts_reorder(request):
        parts = Parts().get_reorder_items()
        return render_to_response('parts_reorder.html',{'parts': parts}, context_instance=RequestContext(request))

def reports_view_all(request):
        return render_to_response('reports_view_all.html',{}, context_instance=RequestContext(request))

def locations_view_all(request):
        locations_list = Locations.objects.all()
        paginator = Paginator(locations_list, 10)

        try:
                page = int(request.GET.get('page', '1'))
        except ValueError:
                page = 1

        try:
                locations = paginator.page(page)
        except (EmptyPage, InvalidPage):
                locations = paginator.page(paginator.num_pages)

        return render_to_response('locations_view_all.html',{'locations': locations}, context_instance=RequestContext(request))

def locations_edit(request,locationID):
        location = Locations.objects.get(pk=locationID)
        if request.POST:
                form = LocationsForm(data=request.POST, instance=location)
                if form.is_valid():
                        form.save()
                        return HttpResponseRedirect('/locations/view/%d/' % location.id)

        form = LocationsForm(instance=location)
        return render_to_response('locations_edit.html',{'form': form}, context_instance=RequestContext(request))

def locations_add(request):
        if  request.POST:
                form = LocationsForm(data=request.POST)
                if form.is_valid():
                        try:
                                newLocation = form.save()
                        except:
                                pass
                        return HttpResponseRedirect('/locations/view/%d/' % newLocation.id)
        else:
                form = LocationsForm()

        return render_to_response('locations_add.html',{'form': form}, context_instance=RequestContext(request))

def locations_view(request, locationID):
        location = Locations.objects.get(pk=locationID)
        return render_to_response('locations_view.html', {'location': location}, context_instance=RequestContext(request))

def logout_view(request):
        logout(request)
        return HttpResponseRedirect('/parts')
