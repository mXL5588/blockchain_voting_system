from django import forms
from django.forms import ModelForm
from .models import VotersList


class VotersListForm(ModelForm):
    class Meta:
        model = VotersList
        fields = ['voters']