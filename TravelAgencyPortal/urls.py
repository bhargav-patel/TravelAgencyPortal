from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TravelAgencyPortal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^user/', include('authentication.urls')),	
	url(r'^portal/', include('portal.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$','portal.views.home',name='home'),
)
