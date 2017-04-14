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

    url(r'^$', views.IndexView.as_view(), name='index'),


    url(r'^login/$', views.LoginView.as_view(), name='login'),

    url(r'^about/$', views.AboutView, name='about'),

    url(r'^chart/(?P<pk>[0-9]+)/$', views.model_property, name='chart'),
    
    url(r'^loginsubmit/$', views.LoginSubmit, name='loginsubmit'),

    url(r'^allresults/$', views.AllResults.as_view(), name='allresults'),

	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

	url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),

	url(r'^(?P<ballot_id>[0-9]+)/vote/$', views.vote, name='vote'),

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
