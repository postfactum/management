from django.conf.urls import url, include
from tastypie.api import Api

from appointments import views as app_views
from appointments.api import AppointmentResource, RangeResource


v1_api = Api(api_name='v1')
v1_api.register(AppointmentResource())
v1_api.register(RangeResource())

urlpatterns = [
	url(r'^api/', include(v1_api.urls)),
	url(r'^appointment/(?P<pk>\d+)/$', app_views.appointment_view),
	url(r'^appointment/create/$', app_views.appointment_create),
    url(r'^reservations/$', app_views.filled_forms),
]

