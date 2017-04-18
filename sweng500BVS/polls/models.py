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
	('mygJdFGURTEsNLZs4tUuxBHmTxnriH3i6y','contestant3Address'),
	('n4P1Hzeis1AdWSp8d3xrDmPepatKmQL7Pz','contestant4Address'),
	('mgVAPC3Yow3K2wDx8bP25XrXbd1G5nvqyn','contestant5Address')
	)

VOTER_ADDRESSES = (
	('mpMtRQUB9XeyXiJevZL6TuLxbvNJJys74j','Voter1Address'),
	('miyLyx2bp4buCnRV4y93RKNH3Lp1s89zQa','Voter2Address'),
	('n39HtcDLnXrxNH4yEra8K7QfVKLN2CJ3Sk','Voter3Address'),
	('mprd13H5FSBYH51Eznvhhwn89Mkny9u1zH','Voter4Address'),
	('mm7LYV3aNxEd45RcgGU7WD29JPqcBRBUSn','Voter5Address'),
	('mz7fyLU79MWuCo6vZTyhEnGbsAbr64J5BB','Voter6Address'),
	('mjzUjupW4LdNb56mNnj9DNDjpagowjgY99','Voter7Address'),
	('mocxZTDcRP1XtBFc3EeAqScF1ahCmVV7uH','Voter8Address'),
	('mzEa7GNeM4a77z5h9maWZVP9NKUaAvJo7h','Voter9Address'),
	('mqE9f1YBdSkoovUQmQ1WCUoRbDWxt2tTtf','Voter10Address'),
	('msf3JRk8aATVzKafhS1XE9eXLyWvNfgEQc','Voter11Address'),
	('n4eRLRVVMXzEjWyhpPtJiQkJroX3NMydvj','Voter12Address'),
	('mgsG2zssbMXKdDebSMCDDqC38wrkJZdB7V','Voter13Address'),
	('mjxBEdw3cTZEdqADtv3TVGQMYJ4Ug6mMey','Voter14Address'),
	('mh5uSJz9peDod9k4eDvCnDJreSBhMZXcUg','Voter15Address'),
	('mxTBS9bmg2xToB3mrVjUBAhiZZyPi9Wy5u','Voter16Address'),
	('mtfS7aoiURB8gwF3sBVdF2frEE8sdMrRJP','Voter17Address'),
	('mwZ4nP3ZcUbAsD9nxQiih9Q3i7XcWTBcAX','Voter18Address'),
	('mgaSJrRHGzPsCGxvWoZXwSzyWfG1m3pfqe','Voter19Address'),
	('mxmfKdzYyxxjD1rz9rba7hBqWsfbbVSEcN','Voter20Address'),
	)

VOTER_NAMES = (
	('Voter1','Voter1'),
	('Voter2','Voter2'),
	('Voter3','Voter3'),
	('Voter4','Voter4'),
	('Voter5','Voter5'),
	('Voter6','Voter6'),
	('Voter7','Voter7'),
	('Voter8','Voter8'),
	('Voter9','Voter9'),
	('Voter10','Voter10'),
	('Voter11','Voter11'),
	('Voter12','Voter12'),
	('Voter13','Voter13'),
	('Voter14','Voter14'),
	('Voter15','Voter15'),
	('Voter16','Voter16'),
	('Voter17','Voter17'),
	('Voter18','Voter18'),
	('Voter19','Voter19'),
	('Voter20','Voter20'),
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
	sendHex = models.CharField(max_length=366, default='None')
	sendAddr = models.CharField(max_length=36, default='None')
	
	def __str__(self):
		return self.voter_name

class ContestantChoice(models.Model):
	ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE,related_name="contestants", related_query_name="contestants")
	contestant_name = models.CharField(max_length=200)
	contestant_address = models.CharField(max_length=36, choices= CONTESTANT_ADDRESSES)
	votes = models.IntegerField(default=0)
	confirmedVotes = models.IntegerField(default=0)
	unconfirmedVotes = models.IntegerField(default=0)
	
	def __str__(self):
		return self.contestant_name

class VotersList(models.Model):
	votersList_name = models.CharField(max_length=200)
	currentVoterChoice = models.CharField(max_length=36)
	def __str__(self):
		return self.votersList_name

class VotersListChoice(models.Model):
	voterlist = models.ForeignKey(VotersList, on_delete=models.CASCADE,related_name="listvoters", related_query_name="listvoters")

	voter_name = models.CharField(max_length=200, choices=VOTER_NAMES)
	voter_address = models.CharField(max_length=36, choices=VOTER_ADDRESSES)
	def __str__(self):
		return self.voter_name

