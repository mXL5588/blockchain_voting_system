from django import forms
from django.forms import ModelForm
from .models import VotersList

VOTER_ADDRESSES = (
	('Voter1Address','mpMtRQUB9XeyXiJevZL6TuLxbvNJJys74j'),
	('voter2Address','miyLyx2bp4buCnRV4y93RKNH3Lp1s89zQa'),
	('voter3Address','n39HtcDLnXrxNH4yEra8K7QfVKLN2CJ3Sk'),
	('voter4Address','n39HtcDLnXrxNH4yEra8K7QfVKLN2CJ3Sk'),
	)


class VotersListForm(forms.ModelForm):
	error_css_class  = 'error'
	voters = forms.ChoiceField(choices=VOTER_ADDRESSES,required=True)

	class Meta:
		model = VotersList
		fields = "__all__"