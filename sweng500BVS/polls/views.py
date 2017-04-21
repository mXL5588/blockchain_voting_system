from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.template import loader
from django.shortcuts import render
from .models import Ballot, VoterChoice, ContestantChoice, VotersList, VotersListChoice
from django.views import generic
from .counterparty import *
from datetime import datetime 
from django.utils import timezone
from django.views.generic import FormView  
from chartit import DataPool, Chart
import functools


def Vote(request, ballot_id):
	#return HttpResponse("You're voting on ballot %s" % ballot_id)
	ballot = get_object_or_404(Ballot, pk=ballot_id)
	print("Ballot Name: ", ballot.ballot_name)
	try:
		selected_choice = ballot.contestants.get(pk=request.POST['choice'])

	except (KeyError, ContestantChoice.DoesNotExist):
		# Redisplay the ballot voting form
		return render(request, 'polls/detail.html', 
			{ 'ballot': ballot, 'error_message': "You didn't select a choice.",})
	else:
		voterList = VotersList.objects.all()[0]
		validCheck = validateAddress(selected_choice.contestant_address)
		response = createSend(voterList.currentVoterChoice, selected_choice.contestant_address, ballot.ballot_name)
		jsonObj = json.loads(response.text)
		if 'error' not in jsonObj:
			print("Response 1: ", jsonObj)
			response = signRawTransaction(jsonObj['result'])
			#Save this hex value to use it for finding unconfirmed transaction
			for voter in ballot.voters.all():
				if voterList.currentVoterChoice == voter.voter_address:
					voter.sendHex = getXCPTxInfo(jsonObj['result'])
					voter.sendAddr = getXCPDestAddr(jsonObj['result'])
					voter.save()


			#print("Length: ",len(jsonObj['result']))

			jsonObj = json.loads(response.text)
			if 'error' in jsonObj:
				print("Response 2: ", jsonObj)
				response = sendRawTransaction(jsonObj['result']['hex'])
				jsonObj = json.loads(response.text)
				if 'error' in jsonObj:
					print("Response 3: ", jsonObj)
					for contestant in ballot.contestants.all():
						contestant.unconfirmedVotes = 0
						contestant.save()
					for voter in ballot.voters.all():
						# print("Voter send hex", voter.sendHex)
						# if voter.sendHex != 'None':
						# 	print ("Unconfirmed Qty: ", getUnconfirmedQuantity(voter.sendHex))
						# 	print("Ballot Candidate Balance: ", getBallotCandidateBalance(voter.voter_address,ballot.ballot_name))
						if voter.sendHex != 'None' and getUnconfirmedQuantity(voter.sendHex) == 1 and getBallotCandidateBalance(voter.voter_address,ballot.ballot_name) == 1:
							print("Unconfirmed exists")
							for contestant in ballot.contestants.all():
								if contestant.contestant_address == voter.sendAddr:
									contestant.unconfirmedVotes = contestant.unconfirmedVotes + 1
									contestant.save()
				else:
					print("Error-3 Response: ", jsonObj)
			else:
				print("Error-2 Response: ", jsonObj)
		else:
			print("Error-1 Response: ", jsonObj)


		# Always return an HTTPResponseRedirect after successfully dealing 
		# with POST data. This prevents data from being posted twice if a
		# user hits the back button.

		return HttpResponseRedirect(reverse('polls:results', args=(ballot.id,)))



def LoginSubmit(request):
	voterList = VotersList.objects.all()[0]
	# try:
	# 	selected_choice = voterList.listvoters.get(pk=request.POST['inputUserName'])

	# except (KeyError, VotersListChoice.DoesNotExist):
	# 	# Redisplay the ballot voting form
	# 	return render(request, 'polls/login.html',
	# 		{ 'voterList': voterList, 'error_message': "You didn't select a choice.",})
	# else:
	# 	voterList.currentVoterChoice = selected_choice.voter_address;
	# 	voterList.save()
	# 	# Always return an HTTPResponseRedirect after successfully dealing 
	# 	# with POST data. This prevents data from being posted twice if a
	# 	# user hits the back button.
	for voter in voterList.listvoters.all():
		if voter.voter_name == request.POST['inputUserName']:
			if voter.voter_name == request.POST['inputPassword']:
				voterList.currentVoterChoice = voter.voter_address;
				voterList.save()
				return HttpResponseRedirect(reverse('polls:index'))
			else:
				return render(request, 'polls/login.html',
					{ 'voterList': voterList, 'error_message': "Invalid user name or password",})
	return render(request, 'polls/login.html',
		{ 'voterList': voterList, 'error_message': "Invalid user name or password",})


		


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_ballot_list'

	def get_queryset(self):
		voterList = VotersList.objects.all()[0]
		list = getAssetList(voterList.currentVoterChoice)
		voterAddress = (voterList.currentVoterChoice)
		ballotList = []
		for name in list:
			for ballot in Ballot.objects.all():
				if name == ballot.ballot_name:
					balanceCheck = getAssetBalance(voterAddress, name)
					if balanceCheck >= 1:
						for voter in ballot.voters.all():
							if voterList.currentVoterChoice == voter.voter_address:
								if voter.sendHex == 'None':
									ballotList.append(ballot)
								else:
									if getUnconfirmedQuantity(voter.sendHex) != 1:
										ballotList.append(ballot)
									else:
										print("Unconfirmed transaction not added")
		return ballotList

class LoginView(generic.ListView):
	template_name = 'polls/login.html'
	context_object_name = 'voters_list'

	def get_queryset(self):
		return VotersList.objects.all()



class AllResults(generic.ListView):
	template_name = 'polls/allResults.html'
	context_object_name = 'all_ballots_list'

	def get_queryset(self):
		for ballot in Ballot.objects.all():
			
			for contestant in ballot.contestants.all():
				contestant.unconfirmedVotes = 0
				contestant.save()

			for voter in ballot.voters.all():
				if voter.sendHex != 'None' and getUnconfirmedQuantity(voter.sendHex) == 1 and getBallotCandidateBalance(voter.voter_address,ballot.ballot_name) == 1:
					for contestant in ballot.contestants.all():
						#print(ballot.ballot_name, " ", contestant.contestant_address, " ", voter.sendAddr)
						if contestant.contestant_address == voter.sendAddr:
							contestant.unconfirmedVotes = contestant.unconfirmedVotes + 1
							contestant.save()
		return Ballot.objects.all()


class DetailView(generic.DetailView):
	model = Ballot
	template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
	model = Ballot
	template_name = 'polls/results.html'
	

def AboutView(request):
	template_name = 'polls/about.html'
	return render(request, 'polls/about.html')


def HomeView(request):
	template_name = 'polls/home.html'
	return render(request, 'polls/home.html')


def BarChart(request, pk):
	allBallot = Ballot.objects.all()
	ballot = Ballot.objects.get( id=pk )

	for c in ballot.contestants.all():
		c.confirmedVotes = getBallotCandidateBalance(c.contestant_address, ballot.ballot_name)
		c.save()

	dataSource = DataPool(
			series=[{
				'options': {
			    	'source': ballot.contestants.all(),
			    },
			    'terms': [
			    	'contestant_name',
			    	'confirmedVotes',
			    	'unconfirmedVotes'
			    ]
			}]
	)

	chart = Chart(
			datasource=dataSource,
			series_options=[{
				'options': {
					'type': 'column',
					'stacking': True,
					'stack': 0,
	            },
			    'terms': {
					'contestant_name': [
						'confirmedVotes',
						'unconfirmedVotes'
					]
				}}
			],
			chart_options={
				'title': {
					'text': ballot.ballot_name
				},
				'xAxis': {
					'title': {
						'text': 'Contestants'
					}
				}
			}
	)
	return render_to_response('polls/graph.html',
							{
							'chart_list': chart,
							'title': 'Ballot statistics'}, pk)