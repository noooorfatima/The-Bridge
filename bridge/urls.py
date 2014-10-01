from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin
admin.autodiscover()
from bridge import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bridge.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.IndexView, name='index'),
    (r'^favicon\.ico$', RedirectView.as_view(url='/static/images/bridge_favicon.ico')),
    #url(r'^$', 'bridge.views
    url(r'^words_page/?$', views.words_page),
    url(r'^greek_words_page/?$', views.greek_words_page),
    url(r'^latin_book_select/?$', views.latin_language_select),
    url(r'^greek_book_select/?$', views.greek_language_select),
#    url(r'^books_page/?$', views.books_page),
    url(r'^about$', views.AboutView.as_view(), name='about'),
    url(r'^help$', views.HelpView.as_view(), name='help'),
    url(r'^contact$', views.ContactView.as_view(), name='contact'),
    url(r'^admin/', include(admin.site.urls)),
)
