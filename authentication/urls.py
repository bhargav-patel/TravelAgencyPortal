from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'register/', 'authentication.views.register',name='register'),
    url(r'login/', 'authentication.views.login_view',name='login'),
    url(r'logout/', 'authentication.views.logout_view',name='logout'),
    url(r'logout/', 'authentication.views.logout_view',name='logout'),
    url(r'^(?P<username>\w+)/$', 'authentication.views.profile_page', name='profile_page'),
)