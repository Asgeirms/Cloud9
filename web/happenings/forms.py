from django import forms
from .models import Event, Schedule


class EventForm(forms.ModelForm):
    '''Formclass. Creating event suggestions'''

    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['end_time'].widget.attrs.update({'autocomplete': 'off'})

    class Meta:
        model = Event
        exclude = ['admin_approved']
        labels = {
            'min_price': 'Minimum price',
            'max_price': 'Maximum price'
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name of the event'}),
            'location': forms.TextInput(attrs={'placeholder': 'Where to host?'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe your event!'}),
        }

        def clean(self):
            cleaned_data = super().clean()
            start_time = cleaned_data.get('start_time')
            end_time = cleaned_data.get('end_time')

            # Validating the time fields
            if start_time > end_time:
                self.add_error(
                    'start_time',
                    forms.ValidationError("Start time cannot begin after end time!"),
                    code='invalid_time'
                )
            return cleaned_data

        def save(self, commit=True):
            """Coupling Schedule and Event. """

            # Happens when user is submitting the form.
            # Need to save the event first
            event = super().save(commit=commit)

            # Linking the saved event to a schedule object
            event_schedule = Schedule.objects.create(
                start_time=self.cleaned_data['start_time'],
                end_time=self.cleaned_data['end_time'],
                event=event
            )
