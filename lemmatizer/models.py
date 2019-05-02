from django.db import models
from django.core.files.storage import FileSystemStorage
import random
import os
from django.db.models.fields.files import FieldFile

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


class lemmmatizer(models.Model):
        LATIN = 'latin'
        GREEK = 'greek'
        LANGUAGE_CHOICES = ((LATIN, 'Latin'), (GREEK, 'Greek'))

        language = models.CharField(max_length = 5, choices=LANGUAGE_CHOICES, default=LATIN)
        created_at = models.DateTimeField(auto_now_add=True)
#changed the below line
        file = models.FileField(blank=False, storage=FileSystemStorage(location='/tmp/lematizer_temp_file.txt'))
        text = models.TextField(default='', blank=True)
        #print(os.path.basename(file.name))
        #print(FieldFile.name)
       # x = FieldFile(file)
       # print(x.name)
        BRIDGE = 'bridge'
        MORPHEUS = 'morpheus'
        FORMAT_CHOICES = ((BRIDGE, 'Bridge'), (MORPHEUS, 'Morpheus'))
        lem_format = models.CharField(max_length = 8, choices=FORMAT_CHOICES, default=BRIDGE)

        AMBIGUOUS = 'Ambiguous'
        UNAMBIGUOUS = 'Unambiguous'
        FORMAT_CHOICES = ((AMBIGUOUS, 'Ambiguous'), (UNAMBIGUOUS, 'Unambiguous'))

        lem_level = models.CharField(max_length = 11, choices=FORMAT_CHOICES, default=AMBIGUOUS)

        CSV = 'csv'
        EXCEL = 'Excel'
        FORMAT_CHOICES = ((CSV, 'csv'), (EXCEL, 'Excel'))

        out_format = models.CharField(max_length = 5, choices=FORMAT_CHOICES, default=EXCEL)
    
        question = models.CharField(max_length=15, default=romanMath())

    # i would think you would add something about the language here... 
    # later on if lemmatizer.language == 'latin': is asked  
class formatlemmatizedtext(models.Model):
	
	created_at = models.DateTimeField(auto_now_add=True)

	file = models.FileField(blank=True, storage=FileSystemStorage(location='/tmp/format_temp_file.txt'))
	
	CSV = 'csv'
	EXCEL = 'Excel'
	FORMAT_CHOICES = ((CSV, 'csv'), (EXCEL, 'Excel'))

	in_format = models.CharField(max_length = 5, choices=FORMAT_CHOICES, default=EXCEL)

	CSV = 'csv'
	EXCEL = 'Excel'
	FORMAT_CHOICES = ((CSV, 'csv'), (EXCEL, 'Excel'))

	out_format = models.CharField(max_length = 5, choices=FORMAT_CHOICES, default=CSV)
    
	question = models.CharField(max_length=17, default=romanMath())

