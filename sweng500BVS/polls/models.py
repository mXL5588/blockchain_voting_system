from __future__ import unicode_literals


from django.db import models
#from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import datetime
# Create your models here.


class Ballot(models.Model):
	ballot_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	end_date = models.DateTimeField('end date')
	def __str__(self):
		return self.ballot_text

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
	ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	choice_address = models.CharField(max_length=36)
	votes = models.IntegerField(default=0)
	
	def __str__(self):
		return self.choice_text



