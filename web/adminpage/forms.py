from django import forms

from happenings.models import GeneratedShortDescriptions, InterestCategory, RequirementCategory


class GeneratedShortDescriptionsForm(forms.ModelForm):
    class Meta:
        model = GeneratedShortDescriptions
        fields = '__all__'

        labels = {
            'description': 'A funny, short, clickbait description',
        }


class InterestCategoryForm(forms.ModelForm):
    class Meta:
        model = InterestCategory
        fields = '__all__'


class RequirementCategoryForm(forms.ModelForm):
    class Meta:
        model = RequirementCategory
        fields = '__all__'
