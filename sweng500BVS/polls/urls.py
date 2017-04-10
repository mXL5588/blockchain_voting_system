from django.conf.urls import url
from .charts import model_property

from . import views

app_name = 'polls'
sort_order = {
    'Welcome': 0,
    'Charts': 1,
    'Pivot Charts': 2,
    'Charts w/ RawQuerySet': 3,
}
sidebar_items = []
urlpatterns = [
	# ex: /polls/
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),


    url(r'^login/$', views.LoginView.as_view(), name='login'),

    url(r'^chart/$', model_property,
    {
        'title': 'Column chart',
        'sidebar_section': 'Charts',
    },
    name='column_chart',
    ),
    
    url(r'^loginsubmit/$', views.LoginSubmit, name='loginsubmit'),

    url(r'^allresults/$', views.AllResults.as_view(), name='allresults'),

    # ex: /polls/5/
    # the 'name' value as called by the {$ url $} template tag
    #url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # ex: /polls/5/results/
	#url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
	url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),

    # ex: /polls/5/vote/
	url(r'^(?P<ballot_id>[0-9]+)/vote/$', views.vote, name='vote'),

    url(r'^charts/$', views.barchart, name='chart'),

]

# build sidebar_items first
seen_sections = []
for u in urlpatterns:
    if u.default_args:
        section = u.default_args['sidebar_section']
        title = u.default_args['title']

        # check if we've seen this section already
        if section not in seen_sections:
            item = {
                'sort_order': sort_order[section],
                'section': section,
                'links': [],
            }
            sidebar_items.append(item)
            seen_sections.append(section)

        # now add the new link to the sidebar section
        for item in sidebar_items:
            if item['section'] == section:
                item['links'].append((title, u.name))
                break

        del u.default_args['sidebar_section']

# now assign sidebar_items to urls
for u in urlpatterns:
    if u.default_args:
        u.default_args['sidebar_items'] = sidebar_items
