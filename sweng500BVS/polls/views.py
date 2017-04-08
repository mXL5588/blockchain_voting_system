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
from .counterparty import createIssuance, createSend, signRawTransaction, sendRawTransaction, getBalance


# Create your views here.
#def hour(request):
	#now = datetime.now()
	#testlist = ['Bern','Bob','Eufronio','Epifanio','El pug']
	#return render(request, 'polls/index.html', {"list": list})
	#return render_to_response({"testlist": testlist})

# Create your views here.



# def post_list(request):
#     posts = 'Bern'
#     return render(request, 'polls/index.html',{'tests': posts})

# def current_datetime(request):
# 	html = "It is now test." 
# 	return HttpResponse(html)

def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()

def vote(request, ballot_id):
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
		response = createSend(voterList.currentVoterChoice, selected_choice.contestant_address, ballot.ballot_name)
		jsonObj = json.loads(response.text)
		if 'error' not in jsonObj:
			print("Response 1: ", jsonObj)
			response = signRawTransaction(jsonObj['result'])
			jsonObj = json.loads(response.text)
			if 'error' in jsonObj:
				print("Response 2: ", jsonObj)
				response = sendRawTransaction(jsonObj['result']['hex'])
				jsonObj = json.loads(response.text)
				if 'error' in jsonObj:
					print("Response 3: ", jsonObj)
					print("Balance for ", selected_choice.contestant_name, ":", getBalance(selected_choice.contestant_address, ballot.ballot_name))
				else:
					print("Error-3 Response: ", jsonObj)
			else:
				print("Error-2 Response: ", jsonObj)
		else:
			print("Error-1 Response: ", jsonObj)
		selected_choice.votes += 1
		selected_choice.save()

		# Always return an HTTPResponseRedirect after successfully dealing 
		# with POST data. This prevents data from being posted twice if a
		# user hits the back button.

		return HttpResponseRedirect(reverse('polls:results', args=(ballot.id,)))



def LoginSubmit(request):
	voterList = VotersList.objects.all()[0]
	try:
		selected_choice = voterList.listvoters.get(pk=request.POST['choice'])

	except (KeyError, VotersListChoice.DoesNotExist):
		# Redisplay the ballot voting form
		return render(request, 'polls/login.html',
			{ 'voterList': voterList, 'error_message': "You didn't select a choice.",})
	else:
		voterList.currentVoterChoice = selected_choice.voter_address;
		voterList.save()
		# Always return an HTTPResponseRedirect after successfully dealing 
		# with POST data. This prevents data from being posted twice if a
		# user hits the back button.

		return HttpResponseRedirect(reverse('polls:index'))


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_ballot_list'

	def get_queryset(self):
		#voterslist = .objects.all()
		"""Return the last five published ballot"""
		print("*********************Ballots returned reached********************************")
		voterList = VotersList.objects.all()[0]
		list = getAssetList(voterList.currentVoterChoice)
		ballotList = []
		for name in list:
			for ballot in Ballot.objects.all():
				if name == ballot.ballot_name:
					ballotList.append(ballot)

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
		return Ballot.objects.all()


# class LoginView(FormView):
# 	template_name = 'polls/login.html'
# 	form_class = VotersListForm

# 	def form_valid(self, form):
# 		print("Voter Address: ", VotersListForm.voters)
# 		return HttpResponseRedirect(reverse('polls:index'))
# 	template_name = 'polls/login.html'
# 	model = VotersList
# 	form_class = VotersListForm

# def LoginView(request):
# 	form = VotersListForm(request.POST or None)
# 	if form.is_valid():
# 		print(form.cleaned_data.get('voters'))
# 	print(request.session.get('voters'))
# 	return render(request, 'polls/login.html')


class DetailView(generic.DetailView):
	model = Ballot
	template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
	model = Ballot
	template_name = 'polls/results.html'
	