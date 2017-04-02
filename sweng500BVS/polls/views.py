from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.template import loader
from django.shortcuts import render
from .models import Ballot, VoterChoice, ContestantChoice, VotersList
from .forms import VotersListForm
from django.views import generic
from .counterparty import *
from datetime import datetime 
from django.utils import timezone


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

	try:
		selected_choice = ballot.contestants.get(pk=request.POST['choice'])

	except (KeyError, ContestantChoice.DoesNotExist):
		# Redisplay the ballot voting form
		return render(request, 'polls/detail.html', 
			{ 'ballot': ballot, 'error_message': "You didn't select a choice.",})
	else:
		selected_choice.votes += 1
		selected_choice.save()

		# Always return an HTTPResponseRedirect after successfully dealing 
		# with POST data. This prevents data from being posted twice if a
		# user hits the back button.

		return HttpResponseRedirect(reverse('polls:results', args=(ballot.id,)))


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_ballot_list'

	def get_queryset(self):
		"""Return the last five published ballot"""
		return Ballot.objects.order_by('-pub_date')[:5]


def LoginView(request):
	return render(request, 'polls/login.html')
	# template_name = 'polls/login.html'
	# model = VotersList
	# form_class = VotersListForm

def search(request):
	if request.method == 'POST':
		search_id = request.POST.get('polls:textfield', None)
		print(search_id)
		html = ("<H1>%s</H!>",search_id)
		return render(request, 'polls/login.html')
	else:
		return render(request, 'polls/login.html')


class DetailView(generic.DetailView):
	model = Ballot
	template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
	model = Ballot
	template_name = 'polls/results.html'
	