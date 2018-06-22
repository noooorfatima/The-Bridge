from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib import admin

from new_bridge import views, settings
from lemmatizer import views as lemviews


urlpatterns = [
    # Example:
    #path('somestring_with/<variables>', 'something in views', name='name of thing in views (optional)'),
    #path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),
    path('admin/', admin.site.urls),
    path('', views.IndexView, name='index'),
    path('admin/import', views.myimport),
    path('favicon.ico', RedirectView.as_view(url = settings.STATIC_URL + 'favicon.ico')),
    path('words_page_redirect/<language>/', views.words_page_redirect),
    path('words_page/<language>/<text>/<bookslist>/<text_from>/<text_to>/<add_remove>/', views.words_page),
    path('get_words/<language>/<text>/<bookslist>/<text_from>/<text_to>/<add_remove>/', views.get_words),
    path('about', views.AboutView),
    path('lemmatizer/', lemviews.lemmatizer, name='lemmatizer'), 
    path('lemmatized', lemviews.lemmatizer, name='lematized'),
    path('format/', lemviews.formatlemmatizedtext, name='format'),
    path('formatted/', lemviews.formatlemmatizedtext, name='formatted'),
]

