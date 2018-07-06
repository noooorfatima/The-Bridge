from django import forms
from django.db import models
from dal import autocomplete
from new_bridge import models
"""
Both of these search TextMetadata based on the name for humans. However, in the meta fields, call it books or texts, because that is what displays to the user. Calling it texts would be better, but for some reason that is throwing an error and books isn't (although based on the the error for texts, neither one should work)
"""
def get_choice_list_latin():
    return [text.name_for_humans for text in models.TextMetadata.objects.filter(language='latin')]
def get_choice_list_greek():
    return [text.name_for_humans for text in models.TextMetadata.objects.filter(language='greek')]

class TextMetadataAutoForm_latin(forms.ModelForm):

    books = autocomplete.Select2ListCreateChoiceField(
        choice_list = get_choice_list_latin,
        required = False,
        widget = autocomplete.ListSelect2(url='book_lookup_latin')
    )
    class Meta:
        fields = ['books']
        model = models.TextMetadata

class TextMetadataAutoForm_greek(forms.ModelForm):

    books = autocomplete.Select2ListCreateChoiceField(
        choice_list = get_choice_list_greek,
        required = False,
        widget = autocomplete.ListSelect2(url='book_lookup_greek')
    )
    class Meta:
        fields = ['books']
        model = models.TextMetadata
