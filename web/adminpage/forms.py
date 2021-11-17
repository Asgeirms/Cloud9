from django import forms

from happenings.models import GeneratedShortDescriptions, EventCategory, AccessibilityTag


class GeneratedShortDescriptionsForm(forms.ModelForm):
    """This form is used for the creation and updating for the predefined short descriptions"""
    class Meta:
        model = GeneratedShortDescriptions
        fields = '__all__'

        labels = {
            'description': 'A funny, short, clickbait description',
        }


class EventCategoryForm(forms.ModelForm):
    """This form is used for the creation and updating for the event categories"""
    class Meta:
        model = EventCategory
        fields = '__all__'


class AccessibilityTagForm(forms.ModelForm):
    """This form is used for the creation and updating for the accessibility tags"""
    class Meta:
        model = AccessibilityTag
        fields = '__all__'
