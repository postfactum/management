from django.db import models


class Range(models.Model):

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:

        verbose_name = "Range"
        verbose_name_plural = "Ranges"
        ordering = ('date', 'start_time')

    def __unicode__(self):
        return '{}, {} - {}'.format(self.date, self.start_time, self.end_time)


class Appointment(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    add_info = models.TextField()
    ranges = models.ManyToManyField(Range)

    class Meta:

        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        ordering = ('description',)

    def __unicode__(self):
        return self.name


class Reservation(models.Model):

    appointment = models.ForeignKey(Appointment)
    range = models.ForeignKey(Range)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()

    class Meta:

        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        ordering = ('appointment',)

    def __unicode__(self):
        return '{}, {}'.format(self.full_name, self.appointment)
