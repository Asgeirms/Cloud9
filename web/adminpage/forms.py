from django import forms

from happenings.models import GeneratedShortDescriptions, InterestCategory, RequirementCategory


class GeneratedShortDescriptionsForm(forms.ModelForm):
    """This form is used for the creation and updating for the predefined short descriptions"""
    class Meta:
        model = GeneratedShortDescriptions
        fields = '__all__'

        labels = {
            'description': 'A funny, short, clickbait description',
        }


class InterestCategoryForm(forms.ModelForm):
    """This form is used for the creation and updating for the interest categories"""
    class Meta:
        model = InterestCategory
        fields = '__all__'


class RequirementCategoryForm(forms.ModelForm):
    """This form is used for the creation and updating for the requirement categories"""
    class Meta:
        model = RequirementCategory
        fields = '__all__'
