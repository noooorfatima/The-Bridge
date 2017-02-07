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
    url(r'^admin/import', views.myimport),
    (r'^favicon\.ico$', RedirectView.as_view(url='/static/images/bridge_favicon.ico')),
    url(r'^words_page_redirect/(?P<language>[a-zA-Z]+)/$', views.words_page_redirect),
    url(r'^words_page/(?P<language>[a-zA-Z]+)/(?P<text>[a-zA-Z0-9\%\(\)\,\-\ \.\_\+\'\:\>\!]+)/(?P<bookslist>[a-zA-Z0-9[a-zA-Z0-9\%\(\)\,\-\ \.\_\+\'\:\>\!\$]+)/(?P<text_from>[a-zA-Z0-9 \.]*)/(?P<text_to>[a-zA-Z0-9 \.]*)/(?P<add_remove>[a-zA-Z0-9 ]*)/$', views.words_page),
    url(r'^get_words/(?P<language>[a-zA-Z]+)/(?P<text>[a-zA-Z0-9\%\(\)\,\-\ \.\_\+\'\:\>\!]+)/(?P<bookslist>[a-zA-Z0-9[a-zA-Z0-9\%\(\)\,\-\ \.\_\+\'\:\>\!\$]+)/(?P<text_from>[a-zA-Z0-9 \.]*)/(?P<text_to>[a-zA-Z0-9 \.]*)/(?P<add_remove>[a-zA-Z0-9 ]*)/$', views.get_words),
    url(r'^about$', views.AboutView),
    #url(r'^help$', views.HelpView.as_view(), name='help'),
    #url(r'^contact$', views.ContactView.as_view(), name='contact'),
    url(r'^admin/', include(admin.site.urls)),
)
