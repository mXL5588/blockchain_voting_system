from __future__ import unicode_literals


from django.db import models
#from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import datetime
# Create your models here.

BALLOT_ADDRESSES = (
	('ballot1','mh4w5JnU662ddHywJU3X1wYL6mufjd6Egz'),
	)

VOTER_ADDRESSES = (
	('voter1','mpMtRQUB9XeyXiJevZL6TuLxbvNJJys74j'),
	('voter2','miyLyx2bp4buCnRV4y93RKNH3Lp1s89zQa'),
	('voter3','n39HtcDLnXrxNH4yEra8K7QfVKLN2CJ3Sk'),
	)

class Ballot(models.Model):
	ballot_name = models.CharField(max_length=200)
	ballot_address = models.CharField(max_length=36, choices= BALLOT_ADDRESSES)
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

class Choice(models.Model):
	ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
	voter_text = models.CharField(max_length=200)
	voter_address = models.CharField(max_length=36, choices= VOTER_ADDRESSES)
	#votes = models.IntegerField(default=0)
	
	def __str__(self):
		return self.voter_text



