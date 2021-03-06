from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from hackerspace_management.inventory.views import *
from hackerspace_management.asterisk.views import *

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^hackerspace_management/', include('hackerspace_management.foo.urls')),

    # Uncomment this for admin:
     (r'^$', parts_view_all),
     (r'^admin/(.*)', admin.site.root),
     (r'^locations/$', locations_view_all),
     (r'^locations/new/$', locations_add),
     (r'^locations/view/(\d+)/$', locations_view),
     (r'^locations/edit/(\d+)/$', locations_edit),
     (r'^parts/$', parts_view_all),
     (r'^parts/new/$', parts_add),
     (r'^parts/view/(\d+)/$', parts_view),
     (r'^parts/edit/(\d+)/$', parts_edit),
     (r'^parts/reorder/$', parts_reorder),
     (r'^parts/components/edit/(\d+)/$', parts_components_edit),
     (r'^vendors/$', vendors_view_all),
     (r'^vendors/new/$', vendors_add_edit),
     (r'^vendors/view/(\d+)/$', vendors_view),
     (r'^vendors/edit/(\d+)/$', vendors_add_edit),
     (r'^stock/$', stock_view_all),
     (r'^stock/new/$', stock_add_edit),
     (r'^stock/view/(\d+)/$', stock_view),
     (r'^stock/edit/(\d+)/$', stock_add_edit),
     (r'^reports/$', reports_view_all),
     (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
     (r'^accounts/logout/$', logout_view),
     (r'^auth/add/(\d+)/$', callback_add),
)
