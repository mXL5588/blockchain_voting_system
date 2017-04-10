from chartit import DataPool, Chart
from django.shortcuts import render_to_response
from .models import Ballot
from .counterparty import getBallotCandidateBalance


def model_property(request, title, sidebar_items):
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
                                'title': title,
                                'sidebar_items': sidebar_items})
