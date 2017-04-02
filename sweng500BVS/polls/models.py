from __future__ import unicode_literals


from django.db import models
#from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import datetime
# Create your models here.

BALLOT_ADDRESSES = (
	('mh4w5JnU662ddHywJU3X1wYL6mufjd6Egz','ballot1Address'),
	)

CONTESTANT_ADDRESSES = (
	('mujVHE4aQ21SQDeDmg3kSyg37jFnTprUPy','contestant1Address'),
	('mwxTvJ8zxziSeW7J357QxTWF534QMCEtsY','contestant2Address'),
	)

VOTER_ADDRESSES = (
	('mpMtRQUB9XeyXiJevZL6TuLxbvNJJys74j','Voter1Address'),
	('miyLyx2bp4buCnRV4y93RKNH3Lp1s89zQa','voter2Address'),
	('n39HtcDLnXrxNH4yEra8K7QfVKLN2CJ3Sk','voter3Address'),
	)

class Ballot(models.Model):
	ballot_name = models.CharField(max_length=200)
	ballot_address = models.CharField(max_length=36, choices= BALLOT_ADDRESSES)
	ballot_issued = models.BooleanField(default=False)
	isItVoter = models.BooleanField(default=False)
	pub_date = models.DateTimeField('date published')
	end_date = models.DateTimeField('end date')
	def __str__(self):
		return self.ballot_name

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now
		was_published_recently.admin_order_field = 'pub_date'
		was_published_recently.boolean = True
		was_published_recently.short_description = 'Published recently?'

class VoterChoice(models.Model):
	ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE,related_name="voters", related_query_name="voters")
	voter_name = models.CharField(max_length=200)
	voter_address = models.CharField(max_length=36, choices= VOTER_ADDRESSES)
	
	
	def __str__(self):
		return self.voter_name

class ContestantChoice(models.Model):
	ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE,related_name="contestants", related_query_name="contestants")
	contestant_name = models.CharField(max_length=200)
	contestant_address = models.CharField(max_length=36, choices= CONTESTANT_ADDRESSES)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.contestant_name


class VotersList(models.Model):
  voters = models.CharField(max_length=36, choices=VOTER_ADDRESSES, default='Voter1Address')