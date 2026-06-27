from django import forms
from .models import OrganizationProfile

class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = OrganizationProfile
        fields = ['profile_photo']
