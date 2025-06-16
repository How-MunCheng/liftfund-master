from django import forms
from django.core.exceptions import ValidationError

from .models import *


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        exclude = ('user', 'is_deleted')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['deadline'].input_formats = ['%Y-%m-%d']

    def clean_user(self):
        return self.user


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        exclude = ('date', 'approved', 'campaign')

    def clean_donation(self):
        amount = self.cleaned_data['donation']
        if amount < 5:
            raise ValidationError("Amount must be greater or equal to $5")
        return amount
