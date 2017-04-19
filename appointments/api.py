from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.serializers import Serializer

from .models import Range, Appointment


class RangeResource(ModelResource):

    class Meta:

        queryset = Range.objects.all()
        resource_name = 'ranges'
        allowed_methods = ['get', 'post']
        authorization = Authorization()
        authentication = Authentication()


class AppointmentResource(ModelResource):

    ranges = fields.ToManyField("appointments.api.RangeResource",
                                "ranges", full=True)

    class Meta:

        queryset = Appointment.objects.all()
        resource_name = 'appointments'
        allowed_methods = ['get', 'post']
        authorization = Authorization()
        authentication = Authentication()
