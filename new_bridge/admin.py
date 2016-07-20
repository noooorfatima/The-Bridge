from django.contrib import admin
from models import *
import os

class WordPropertyLatinAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title']

class WordPropertyGreekAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title']

class TextStructureGlossaryAdmin(admin.ModelAdmin):
    search_fields = ['text_name','subsection_level','subsection_name']
    list_display = ['text_name','subsection_level','subsection_name']
    list_filter = ['text_name']

class TextMetadataAdmin(admin.ModelAdmin):
    search_fields = ['name_for_humans','name_for_computers','language','local_def']
    list_display = ['name_for_humans','name_for_computers','language','local_def']

class WordAppearencesLatinAdmin(admin.ModelAdmin):
    search_fields = ['text_name','word','appearance','mindiv']
    list_display = ['text_name','word','appearance','mindiv']
    list_filter = ['text_name']

class WordAppearencesGreekAdmin(admin.ModelAdmin):
    search_fields = ['text_name','word','appearance','mindiv']
    list_display = ['text_name','word','appearance','mindiv']
    list_filter = ['text_name']

class BookTitlesAdmin(admin.ModelAdmin):
    search_fields = ['title_of_book','book_type']
    list_display = ['title_of_book','book_type']
    list_filter = ['book_type']

class BookTitlesGreekAdmin(admin.ModelAdmin):
    search_fields = ['title_of_book','book_type']
    list_display = ['title_of_book','book_type']
    list_filter = ['book_type']

admin.site.register(WordPropertyLatin,WordPropertyLatinAdmin)
admin.site.register(WordPropertyGreek,WordPropertyGreekAdmin)
admin.site.register(TextStructureGlossary,TextStructureGlossaryAdmin)
admin.site.register(TextMetadata,TextMetadataAdmin)
admin.site.register(TextStructureNode)
admin.site.register(WordAppearencesLatin,WordAppearencesLatinAdmin)
admin.site.register(WordAppearencesGreek,WordAppearencesGreekAdmin)
admin.site.register(BookTitles,BookTitlesAdmin)
admin.site.register(BookTitlesGreek,BookTitlesGreekAdmin)


