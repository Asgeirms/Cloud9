from django import forms
from .models import Event, Schedule


class EventForm(forms.ModelForm):
    '''Formclass. Creating event suggestions'''
    class Meta:
        model = Event
        exclude = ['admin_approved', 'host']
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
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')

        # Validating the price fields
        if min_price > max_price:
            self.add_error(
                'min_price',
                forms.ValidationError(
                    "Minimum price cannot cost more than maximum price!",
                    code='invalid_price')
            )
        

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['start_time', 'end_time']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['end_time'].widget.attrs.update({'autocomplete': 'off'})

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        # Validating the time fields
        if start_time > end_time:
            self.add_error(
                'start_time',
                forms.ValidationError(
                    "Start time cannot begin after end time!",
                    code='invalid_time')
            )


class EditEventForm(forms.ModelForm):
    '''Formclass. Creating event suggestions'''

    class Meta:
        model = Event
        exclude = ['admin_approved', 'host', 'name', 'description']
        labels = {
            'min_price': 'Minimum price',
            'max_price': 'Maximum price'
        }
        widgets = {
            'location': forms.TextInput(attrs={'placeholder': 'Where to host?'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')

        # Validating the price fields
        if min_price > max_price:
            self.add_error(
                'min_price',
                forms.ValidationError(
                    "Minimum price cannot cost more than maximum price!",
                    code='invalid_price')
            )
