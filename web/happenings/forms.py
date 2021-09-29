from django import forms
from .models import Event, Schedule


class EventForm(forms.ModelForm):
    '''Formclass. Creating event suggestions'''

    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()
    field_order = ['name', 'location', 'min_price', 'max_price', 'start_time', 'end_time', 'description']

    class Meta:
        model = Event
        exclude = ['admin_approved']
        labels = {
            'min_price': 'Minimum price',
            'max_price': 'Maximum price'
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'location': forms.TextInput(attrs={'placeholder': 'Where to host?'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe your event!'})
        }
    
    def save(self, commit=True):
        """Coupling Schedule and Event. """
        event = super().save(commit=commit)
        event_schedule = Schedule.objects.create(
            start_time=self.cleaned_data['start_time'],
            end_time=self.cleaned_data['end_time'],
            event=event
        )
        event.save()

        return event

