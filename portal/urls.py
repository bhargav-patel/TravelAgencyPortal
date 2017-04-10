from django.conf.urls import patterns, include, url
from portal import views
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = patterns('',
	url(r'^category/$', views.VehCatList.as_view(), name='cat_list'),
	url(r'^category/(?P<pk>\d+)$', views.cat_info, name='cat_info'),
	url(r'^category/new$', staff_member_required(views.VehCatCreate.as_view()), name='cat_new'),
	url(r'^category/edit/(?P<pk>\d+)$', staff_member_required(views.VehCatUpdate.as_view()), name='cat_edit'),
	url(r'^category/delete/(?P<pk>\d+)$', staff_member_required(views.VehCatDelete.as_view()), name='cat_delete'),

	url(r'^vehicle/$', views.VehList.as_view(), name='veh_list'),
	url(r'^vehicle/(?P<pk>\d+)$', views.veh_info, name='veh_info'),
	url(r'^vehicle/bycat/(?P<pk>\d+)$', views.veh_filtered_list, name='veh_filtered_list'),
	url(r'^vehicle/new$', staff_member_required(views.VehCreate.as_view()), name='veh_new'),
	url(r'^vehicle/edit/(?P<pk>\d+)$', staff_member_required(views.VehUpdate.as_view()), name='veh_edit'),
	url(r'^vehicle/delete/(?P<pk>\d+)$', staff_member_required(views.VehDelete.as_view()), name='veh_delete'),

	# url(r'^agency/$', views.VehList.as_view(), name='veh_list'),
	# url(r'^agency/new$', views.VehCreate.as_view(), name='veh_new'),
	url(r'^agency/edit/(?P<pk>\d+)$', staff_member_required(views.AgencyUpdate.as_view()), name='agency_edit'),
	# url(r'^agency/delete/(?P<pk>\d+)$', views.VehDelete.as_view(), name='veh_delete'),

	url(r'^book/(?P<veh_id>\d+)$', views.book_vehicle, name='book'),

	# url(r'^booking/$', staff_member_required(views.BookingList.as_view()), name='booking_list'),
	url(r'^booking/$', views.booking_list, name='booking_list'),
	url(r'^booking/(?P<pk>\d+)$', views.booking_info, name='booking_info'),
	url(r'^booking/(?P<pk>\d+)/return$', views.booking_return, name='booking_return'),
	url(r'^booking/(?P<pk>\d+)/payment$', views.booking_payment, name='booking_payment'),

	url(r'^profile/(?P<pk>\d+)$', views.profile_info, name='profile_info'),
	url(r'^profile/(?P<pk>\d+)/edit$', views.profile_edit, name='profile_edit'),

	url(r'$', 'portal.views.home',name='portal'),
)
