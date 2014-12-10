from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin
admin.autodiscover()
from new_bridge import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bridge.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.IndexView, name='index'),
    (r'^favicon\.ico$', RedirectView.as_view(url='/static/images/bridge_favicon.ico')),
    #url(r'^$', 'bridge.views
    url(r'^words_page/(?P<language>[a-zA-Z]+)/$', views.words_page),
    url(r'^book_select/(?P<language>[a-zA-Z]+)/$', views.book_select),
    url(r'^filter/(?P<language>[a-zA-Z]+)/$', views.filter),
#    url(r'^books_page/?$', views.books_page),
    url(r'^about$', views.AboutView.as_view(), name='about'),
    url(r'^help$', views.HelpView.as_view(), name='help'),
    url(r'^contact$', views.ContactView.as_view(), name='contact'),
    url(r'^admin/', include(admin.site.urls)),
)
