
import os
import xlrd
import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.shortcuts import get_object_or_404, render, redirect
from django.core.files.base import ContentFile
from .utils import handle_uploaded_file
from lemmatizer.forms import PostText, post_text, FormatFile
from lemmatizer import easy_lem
import tempfile
from django.utils.encoding import smart_str
import random
from openpyxl.workbook import Workbook
from openpyxl.reader.excel import load_workbook, InvalidFileException
#from pyparsing import cppStyleComment

#these three functions are part of the captcha that asks a simple math question using Roman numerals.
def roman_solution(value):
    try:
        solution = int(eval(input(question)))
        if type(solution) == type(1) and answer  == solution:
            correct = True
        else:
            correct = False
    except:
            correct = False

def RomToReg(numeral):
    romanNum = ['0','I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI','XVII','XVIII', "XIX", "XX"]
    for i in range(0, len(romanNum)):
            if numeral == romanNum[i]:
                return i

def parseEquation(strInput):
    while " " in strInput:
        strInput = strInput.replace(" ", "")
    question  = strInput.split("=")[0]
    answer = strInput.split("=")[1]
    if "-" in question:
        first = question.split("-")[0]
        second = question.split("-")[1]
        correctAns = RomToReg(first) - RomToReg(second)
    if "+" in question:
        first = question.split("+")[0]
        second = question.split("+")[1]
        correctAns = RomToReg(first) + RomToReg(second)
    givenAns = RomToReg(answer)
    return givenAns == correctAns


#this is the main view for the lemmatizer
def lemmatizer(request):
    if request.method == 'POST':
        form = PostText(request.POST, request.FILES)
        #Next few lines are for filename change
        #using top answer with minor revision: https://stackoverflow.com/questions/3111779/how-can-i-get-the-file-name-from-request-files
        for filename, file in request.FILES.items():
            name = request.FILES[filename].name
	#name='"'+name.split('.')[0]+'"'+name.split('.')[1]
        #print('the name is {}'.format(name))
        name=name.replace(" ", "")
        print('the name is {} now'.format(name))
        name = name.split('.')[0]
        out_name = name + '_lemmatized'
        print('created outname:{}'.format(out_name))


        captcha = str(form['question'].value())
        answer = parseEquation(captcha)
        
        if form.is_valid() and answer:

            language = str(form['language'].value())

            filename = '/tmp/'+out_name+'.txt'
            with open(filename, 'wb') as f:
                """We open a named temporary file from the data in the form. We change the name """
                f.write(form['file'].value().read())
                
                
            with open(filename) as f:
                f.read()
                lem_format = str(form['lem_format'].value())
                out_format = str(form['out_format'].value())
                lem_level = str(form['lem_level'].value())
                easy_lem.lemmatize(language,filename,lem_format,lem_level)
                #pass variables to lemmatize function and Bret's scripts
                #easy_lem.lemmatize(language,filename,lem_format,lem_level)

                #return render(request, 'lemmatized.html', {'form': form, 'output_file': f.name.split('/')[-1].replace('txt','xlsx')})  # ,{'test'='hi1'})
                #Carter's new code below
                if out_format == 'Excel':
                    print('entered the if statement for excel')
                # Here we send the output file to lemmatized.html (tmpEDoVlX_Input.xlsx)
                    if lem_format == 'bridge':
                        output_file = str(f.name).split('.')[0] + '.xlsx'
                        output_file = output_file.split('/')[2]
                        print('created output_file:{}'.format(output_file))




                       # output_file = out_name + '.xlsx'
                    elif lem_format == 'morpheus':
                        output_file = str(f.name).split('.')[0] + '.xlsx'
                        output_file = output_file.split('/')[2]
                        print(output_file)


                        #output_file = out_name + '.xlsx'

                if out_format == 'csv':
                    print('entered the if statement for csv')
                    if lem_format == 'bridge':
                        output_file = str(f.name).split('.')[0] + '.xlsx'
                        #output_file = out_name + '.xlsx'
                        wb = xlrd.open_workbook(output_file)
                      #  print('made it here')
                        sheet_names = wb.sheet_names()
                        sh = wb.sheet_by_name(sheet_names[0])
                        #loc = '/tmp/' + out_name + '.csv'
                        your_csv_file = open('/tmp/lemmatized.csv', 'w')
                        #your_csv_file = open(loc, 'w')
                        wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

                        for rownum in range(sh.nrows):
                            try:
                                wr.writerow(sh.row_values(rownum))
                            except:
                                pass
                        your_csv_file.close()
                        output_file = 'lemmatized.csv'
                        #output_file = out_name + '.csv'


                    elif lem_format == 'morpheus':
                        output_file = str(f.name).split('.')[0] + '.xlsx'
                        wb = xlrd.open_workbook(output_file)
                        sheet_names = wb.sheet_names()
                        sh = wb.sheet_by_name(sheet_names[0])
                        your_csv_file = open('/tmp/lemmatized.csv', 'w')
                        wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

                        for rownum in range(sh.nrows):
                            try:
                                wr.writerow(sh.row_values(rownum))
                            except:
                                pass
                        your_csv_file.close()
                        output_file = 'lemmatized.csv'
                #Remove the tempary txt file, but keep the csv and xlsx output
                    os.unlink(filename)
                    assert not os.path.exists(filename)
            statsfile=open('/tmp/savedata.txt','r')
            contents=statsfile.read()
            statsfile.close()
            return render(request, 'lemmatized.html',{'form':form, 'output_file':output_file,'contents':contents})#,{'test'='hi1'})
    #Remove the tempary txt file, but keep the csv and xlsx output
       # os.unlink(filename)
       # assert not os.path.exists(filename)

#endCarter's new code

        #else:
        #    print((form.errors))
    else:
        form = PostText()
        return render(request, 'lemmatizer.html',{'form':form}) # {'form': form, 'test':'hi2'})

#def lemmatize_file(request):
#    if request.method == 'POST':
#        form = UploadFileForm(request.POST, request.FILES)
#        if form.is_valid():
#            handle_uploaded_file(request.FILES['file'])
##            return HttpResponseRedirect('lemmatize.html')
 #   else:
 #       form = UploadFileForm()

  #  return render(request, 'lemmatized.html', {'form': form,test:'hi4'})
 #   return render(request, 'lemmatize.html', {'form': form})
def formatlemmatizedtext(request):
    if request.method == 'POST':
        cheese = FormatFile(request.POST, request.FILES)
        captcha = str(cheese['question'].value())
        answer = parseEquation(captcha)

        print(answer)
        #print ('Hi, I got to line 174')

        if answer: #cheese.is_valid() and
            #print ('Hi, I got to line 177')

            with tempfile.NamedTemporaryFile(suffix='.xlsx',dir='/tmp/', delete=False) as f:
                f.write(cheese['file'].value().read())#.encode("utf-8"))
                f.flush()
                #TODO: Handle data from textfield
                #f.write(form['text'].value().encode("utf-8"))
                #with .read() gives'unicode' object has no attribute 'read'
                #without gives 'ascii' codec can't encode character u'\u2014' in position 182: ordinal not in range(128)
                #language, filename and format variables from form to pass to easy_lem
                filename = f.name
                print("hello")
                print(filename)
                f.close()


            with open(filename) as f:
                in_format = str(cheese['in_format'].value())
                out_format = str(cheese['out_format'].value())

                #pass variables to lemmatize function and Bret's scripts
                print((filename,in_format,out_format))
                #filename = filename + '.xlsx'

                easy_lem.format(filename)
                print ('Hi, I got to line 203')

                #uncomment to save form data to db
                #form.save(commit=True)

                if out_format == 'Excel':
                #Here we send the output file to lemmatized.html (tmpEDoVlX_Input.xlsx)
                    output_file = str(f.name).split('.')[0] + '_Input.xlsx'
                    output_file = output_file.split('/')[2]


                if out_format == 'csv':
                    output_file = str(f.name).split('.')[0] + '_Input.xlsx'
                    wb = xlrd.open_workbook(output_file)
                    sheet_names = wb.sheet_names()
                    sh = wb.sheet_by_name(sheet_names[0])
                    your_csv_file = open('/tmp/formatted.csv', 'w')
                    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

                    for rownum in range(sh.nrows):
                        try:
                            wr.writerow(sh.row_values(rownum))
                        except:
                            pass
                    your_csv_file.close()
                    output_file = 'formatted.csv'

            return render(request, 'formatted.html',{'cheese':cheese, 'output_file':output_file})#,{'test'='hi1'})
        else:
            print ('Hi, I got to line 238')
            return render(request, 'format.html',{'cheese':cheese})#,{'test'='hi1'})
    else:
        print ('Hi, I got to line 242')

        cheese = FormatFile()
    return render(request, 'format.html',{'cheese':cheese}) # {'form': form, 'test':'hi2'})
def memory_usage_psutil():
    # return the memory usage in percentage like top
    process = psutil.Process(os.getpid())
    mem = process.memory_percent()
    return mem
