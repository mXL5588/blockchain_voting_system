from django.conf.urls import url

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

    url(r'^home/$', views.HomeView, name='home'),
    
    url(r'^about/$', views.AboutView, name='about'),

    url(r'^chart/(?P<pk>[0-9]+)/$', views.BarChart, name='chart'),
    
    url(r'^loginsubmit/$', views.LoginSubmit, name='loginsubmit'),

    url(r'^allresults/$', views.AllResults.as_view(), name='allresults'),

	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

	url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),

	url(r'^(?P<ballot_id>[0-9]+)/vote/$', views.Vote, name='vote'),

]

# build sidebar_items first
seen_sections = []

# now assign sidebar_items to urls
for u in urlpatterns:
    if u.default_args:
        u.default_args['sidebar_items'] = sidebar_items
