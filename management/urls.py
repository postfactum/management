from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from appointments import views as app_views


urlpatterns = [    
    url(r'', include("appointments.urls")),
    url(r'^thanks-page/$', app_views.thanks_page),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'admin/login.html'}),
    url(r'^admin/', include(admin.site.urls)),
]
