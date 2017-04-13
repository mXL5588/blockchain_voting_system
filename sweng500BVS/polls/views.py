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
#from .counterparty import createIssuance, createSend, signRawTransaction, sendRawTransaction, getBalance, getBallotCandidateBalance
from .mycharts import MyBarChartDrawing
from chartit import DataPool, Chart


# Create your views here.

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
		voterAddress = (voterList.currentVoterChoice)
		ballotList = []
		for name in list:
			for ballot in Ballot.objects.all():
				balanceCheck = getAssetBalance(voterAddress, name)
				if name == ballot.ballot_name:
					print("BALANCE ", balanceCheck, name)
					if balanceCheck >= 1:
						print("MATCH")
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
	

def AboutView(request):
	template_name = 'polls/about.html'
	return render(request, 'polls/about.html')

def barchart(request):

    #instantiate a drawing object
    print(request)
    d = MyBarChartDrawing()

    #extract the request params of interest.
    #I suggest having a default for everything.
    if 'height' in request:
        d.height = int(request['height'])
    if 'width' in request:
        d.width = int(request['width'])
    
    if 'numbers' in request:
        strNumbers = request['numbers']
        numbers = map(int, strNumbers.split(','))    
        d.chart.data = [numbers]   #bar charts take a list-of-lists for data

    if 'title' in request:
        d.title.text = request['title']
    d.title.text = 'Basic chart'

    #get a GIF (or PNG, JPG, or whatever)
    binaryStuff = d.asString('gif')
    
    return HttpResponse(binaryStuff, 'image/gif')


def model_property(request):
    print("model_property reached")
    ballot = Ballot.objects.all()[0]
    print("*******************************",ballot.ballot_name)
    for c in ballot.contestants.all():
        print("$$$$$$$$$$$$$$$$$$$$",c.votes)

    ds = DataPool(
            series=[{
                'options': {
                    'source': ballot.contestants.all(),
                },
                'terms': [
                    'contestant_name',
                    'votes'
                ]
            }]
    )

    cht = Chart(
            datasource=ds,
            series_options=[{
                'options': {
                    'type': 'column',
                    'stacking': False,
                    'stack': 0,
                },
                'terms': {
                    'contestant_name': [
                        'votes'
                    ]
                }},
            ],
            chart_options={
                'title': {
                    'text': 'Ballot statistics'
                },
                'xAxis': {
                    'title': {
                        'text': 'Contestants'
                    }
                }
            }
    )
    # end_code
    return render_to_response('polls/graph.html',
                              {
                                'chart_list': cht,
                                'title': "Test Chart"})