from django import forms


class ReservationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.ranges = kwargs.pop('ranges')
        self.dates = kwargs.pop('dates')
        self.timeslots = kwargs.pop('timeslots')

        super(ReservationForm, self).__init__(*args, **kwargs)

        self.fields['dates'] = forms.ChoiceField(
            choices=self.dates, widget=forms.RadioSelect(), label='Choose date')
        self.fields['timeslots'] = forms.ChoiceField(
            choices=self.timeslots, widget=forms.RadioSelect(), label='Choose time')

    full_name = forms.CharField(max_length=200)
    email = forms.EmailField()

    def clean(self):
        # get date checkbutton from current request
        request_date = self.data.get('dates')
        # get timeslot checkbutton from current request
        request_timeslot = self.data.get('timeslots')
        # convert request data to needed format
        request_range = '{}, {}'.format(request_date, request_timeslot)
        # convert API data to needed format
        available_ranges = ['{}, {} - {}'.format(
            range['date'], range['start_time'], range['end_time']) for range in self.ranges]

        if not request_range in available_ranges:
            raise forms.ValidationError(
                """Unfortunally, this combination 
                of date and time isn't available.
                Try to choose another one.""")
        self.cleaned_data['start_time'], self.cleaned_data['end_time'] = tuple(
            request_timeslot.replace(' ', '').split('-'))  # extract start and end times from timeslot

        return self.cleaned_data


class AppointmentForm(forms.Form):

    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    add_info = forms.CharField(widget=forms.Textarea, label='Additional info')
    ranges = forms.CharField(
        widget=forms.Textarea, label="""Ranges: (each range on new line,
                                        format: [date], [start_time] - [end_time])""")

    def clean_ranges(self):
        # list of ranges from form field
        ranges = self.cleaned_data['ranges'].replace(' ', '').split('\r\n')
        response = []

        try:
            for range in ranges:
                separate = range.split(',')  # separate date and timeslot
                result = {}
                result['date'] = separate[0]
                result['start_time'] = separate[1].split('-')[0]  # separate start_time and end_time
                result['end_time'] = separate[1].split('-')[1]  # separate start_time and end_time
                response.append(result)
        except:
            raise forms.ValidationError(
                "Your list of ranges has wrong format. Correct it.")
        return response
