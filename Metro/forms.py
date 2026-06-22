from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['bus_no', 'ward_no', 'location', 'driver_name', 'driver_contact', 'availability']
        widgets = {
            'bus_no': forms.TextInput(attrs={'class': 'p-2 border rounded', 'placeholder': 'Bus No'}),
            'ward_no': forms.NumberInput(attrs={'class': 'p-2 border rounded', 'placeholder': 'Ward No'}),
            'location': forms.TextInput(attrs={'class': 'p-2 border rounded', 'placeholder': 'Location'}),
            'driver_name': forms.TextInput(attrs={'class': 'p-2 border rounded', 'placeholder': 'Driver Name'}),
            'driver_contact': forms.TextInput(attrs={'class': 'p-2 border rounded', 'placeholder': 'Driver Contact'}),
             'availability': forms.Select(choices=Vehicle.AVAILABILITY_CHOICES),
        }