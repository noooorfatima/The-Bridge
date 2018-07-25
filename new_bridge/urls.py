from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib import admin

from new_bridge import views
from new_bridge.views import TextMetadataLookUp_greek
from new_bridge.views import TextMetadataLookUp_latin
from new_bridge import settings
from lemmatizer import views as lemviews


urlpatterns = [
    # Example:
    #path('somestring_with/<variables>', 'something in views', name='name of thing in views (optional)'),
    #path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),
    path('admin/', admin.site.urls),

    path('', views.IndexView, name='index'),
    path('book_lookup_latin',
    TextMetadataLookUp_latin.as_view(),name = "book_lookup_latin"),
    path('book_lookup_greek',
    TextMetadataLookUp_greek.as_view(),name = "book_lookup_greek"),

    path('favicon.ico', RedirectView.as_view(url = settings.STATIC_URL + 'images/bridge_favicon.ico')),
    path('admin/import', views.myimport),
    path('words_page_redirect/<language>/', views.words_page_redirect),
    path('words_page/<language>/<text>/<bookslist>/<text_from>/<text_to>/<add_remove>/', views.words_page),
    path('get_words/<language>/<text>/<bookslist>/<text_from>/<text_to>/<add_remove>/', views.get_words),
    path('about', views.AboutView),
    path('lemmatizer/', lemviews.lemmatizer, name='lemmatizer'),
    path('lemmatizer/Lemmatizer', lemviews.lemmatizer, name='lematized'),
    path('format/', lemviews.formatlemmatizedtext, name='format'),
    path('formatted/', lemviews.formatlemmatizedtext, name='formatted'),
]
