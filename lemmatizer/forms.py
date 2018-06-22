from django import forms
from django.db import models
from django.core.files.storage import FileSystemStorage

import random



from lemmatizer.models import lemmmatizer, formatlemmatizedtext

def romanMath():
    try:
        correct = False
        while (correct == False):
            romanNum = ['0','I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
            length = len(romanNum)
            a = random.randint(1, length)
            b = random.randint(1, length)
            operation = random.randint(1, 2)
            if operation == 1: 
                question = romanNum[a] + " + " + romanNum[b]+ " = "
                answer = a + b
            elif operation == 2: 
                question = romanNum[max(a, b)] + " - " + romanNum[min(a, b)]+ " = "
                answer = max(a, b) - min(a, b)
            return question
    except:
        question = 'I + I = II'
        return question  
        #print "Please solve the roman numeral math problem below, and give your answer in regular numbers."
        

class post_text(forms.Form):
    LATIN = 'latin'
    GREEK = 'greek'
    LANGUAGE_CHOICES = ((LATIN, 'Latin'), (GREEK, 'Greek'))
    language = models.CharField(max_length = 5, choices=LANGUAGE_CHOICES, default=LATIN)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(null=True, storage=FileSystemStorage(location='/tmp/'))
    text = models.TextField(default='')
    ALL = 'all'
    ONLY_UN = 'oun'
    LEVEL_CHOICES = ((ALL,'Lemmatize All Forms'),(ONLY_UN,'Only Unambiguous Forms'))
    lem_level = models.CharField(max_length = 22, choices=LEVEL_CHOICES, default=ALL)
    BRIDGE = 'bridge'
    MORPHEUS = 'morpheus'
    FORMAT_CHOICES = ((BRIDGE, 'Bridge'), (MORPHEUS, 'Morpheus'))
    lem_format = models.CharField(max_length = 8, choices=FORMAT_CHOICES, default=BRIDGE)

class PostText(forms.ModelForm):
        concordance = forms.NullBooleanField()
        class Meta:
                model = lemmmatizer
                fields = ('file','language','out_format','lem_format','lem_level','question')
        file = forms.FileField(label='')

class FormatFile(forms.Form):
    IN_OPTIONS = (
            #("csv", "csv"),
            ("Excel", "Excel"),
            )
    OUT_OPTIONS = (
            ("csv", "csv"),
            ("Excel", "Excel"),
            )
    file = forms.FileField()
    #question = forms.CharField(max_length=17, default=romanMath())
    in_format = forms.MultipleChoiceField(widget=forms.Select,choices=IN_OPTIONS)
    
    out_format = forms.MultipleChoiceField(widget=forms.Select,choices=OUT_OPTIONS)
    fun = romanMath()
    question = forms.CharField(initial=fun)

    

        

