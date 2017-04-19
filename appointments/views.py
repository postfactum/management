from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from .models import Range, Appointment, Reservation
from .forms import AppointmentForm, ReservationForm
from .services import get_ranges


def appointment_view(request, pk):
    # current appointment ranges from API
    ranges = get_ranges(request.META['HTTP_HOST'], pk)
    # correct format to pass it to ChoiceField (+ remove duplicates)
    dates = list(set([(str(key['date']), str(key['date'])) for key in ranges]))
    timeslots = list(set([('{} - {}'.format(key['start_time'], key['end_time']),
                           '{} - {}'.format(key['start_time'], key['end_time'])) for key in ranges]))

    if request.method == 'POST':
        form = ReservationForm(request.POST, ranges=ranges,
                               dates=dates, timeslots=timeslots)

        if form.is_valid():
            data = form.cleaned_data
            app = Appointment.objects.get(id=pk)
            range = Range.objects.get(date=data['dates'], start_time=data['start_time'],
                                      end_time=data['end_time'])

            Reservation.objects.create(
                appointment=app,
                range=range,
                full_name=data['full_name'],
                email=data['email']
            )

            app.ranges.remove(range)

            return HttpResponseRedirect('/thanks-page')

        return render_to_response('appointments/appointment_view.html', {'form': form}, context_instance=RequestContext(request))

    else:
        if ranges:
            form = ReservationForm(ranges=ranges, dates=dates, timeslots=timeslots, initial={
                                   'dates': dates[0][0], 'timeslots': timeslots[0][0]})

            return render_to_response('appointments/appointment_view.html', {'form': form}, context_instance=RequestContext(request))

        else:

            return render_to_response('appointments/appointment_view.html', {'available': False})

@login_required  # built-in authentication system
def appointment_create(request):
    # Interface for appointment creations
    if request.method == 'POST':
        form = AppointmentForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            app = Appointment.objects.create(
                name=data['name'],
                description=data['description'],
                add_info=data['add_info']
            )

            for range in data['ranges']:
                # Prevent duplications creation 
                new_range, created = Range.objects.get_or_create(
                    date=range['date'],
                    start_time=range['start_time'],
                    end_time=range['end_time']
                )

                app.ranges.add(new_range)

            return HttpResponseRedirect('/thanks-page')
    else:
        form = AppointmentForm()

    return render_to_response('appointments/create_appointment.html', {'form': form}, context_instance=RequestContext(request))

@login_required  # built-in authentication system
def filled_forms(request):
    # list of filled forms (for authenticated users)
    reservations = Reservation.objects.all()

    return render_to_response('appointments/reservation_view.html', {'reservations': reservations})

def thanks_page(request):

    return render_to_response('appointments/thanks_page.html')
