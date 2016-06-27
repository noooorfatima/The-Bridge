from django.contrib import admin
from models import WordPropertyLatin,TextStructureGlossary,TextMetadata,WordPropertyGreek,TextStructureNode,WordAppearencesLatin,WordAppearencesGreek,BookTitles
import os
admin.site.register(WordPropertyLatin)
admin.site.register(TextStructureGlossary)
admin.site.register(TextMetadata)
admin.site.register(WordPropertyGreek)
admin.site.register(TextStructureNode)
admin.site.register(WordAppearencesLatin)
admin.site.register(WordAppearencesGreek)
admin.site.register(BookTitles)


