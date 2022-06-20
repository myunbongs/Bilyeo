from django import forms

from bilyeo.models import Category


class StuffForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    fee = forms.IntegerField(required=True)
    image = forms.ImageField(required=True)
    desc = forms.CharField(widget=forms.Textarea(), required=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

class AvailabilityForm(forms.Form):
    rental_date = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])
    return_date = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])

class StuffAvailableForm(forms.Form):
    STUFF_STATUS = (
        ('a', 'available'),
        ('u', 'unavailable'),
    )
    status = forms.ChoiceField(choices=STUFF_STATUS, required=True)

class AcceptForm(forms.Form):
    RENTAL_STATUS = (
        ('d', 'Default'),
        ('r', 'Request'),
        ('a', 'Accept'),
        ('c', 'Completed'),
    )
    status = forms.ChoiceField(choices=RENTAL_STATUS, required=True)