import os
import subprocess
path = os.path.dirname(os.path.realpath(__file__))
import sys 

def lemmatize(language,filename,format,lem_level, concordance):
    print ("in lemmatize in easy_lem.py")
    print((os.environ , "os environ"))
    print(('inputs', language,filename,format,lem_level, concordance))
    try: 
        
        if lem_level == 'Ambiguous':
            key = '-a'
        else:
            key = '' 
        if format == 'bridge':
            ui = '--force-ui'
        else:
            ui = ''
        #subprocess.call('python3 /srv/bridge-repo/lemmatizer/autoLemma.py {0} {1}'.format(language, filename), shell=False)
        #os.system('pip3 install cltk')
        print(("concordance", concordance))
        if concordance: #checks if the input is a concordance
            print ("trying to do a spreadsheet")
            print (filename)
            print (language)
            os.system("python3 /srv/bridge-repo/lemmatizer/lemmatize_spreadsheet.py 'language' 'filename' "  )
        else:
            print((sys.path))
            os.system('python3 /srv/bridge-repo/lemmatizer/autoLemma.py {0} --force-no-punctuation {1} {2} {3}'.format(language,ui, key, filename))

        #convert lemma format to Bridge
        #if language == 'latin':
        #    os.system('python3 /srv/bridge-repo/lemmatizer/convert_lemmata_format.py {0} import /srv/bridge-repo/lemmatizer/morpheus-bridge.xlsx'.format(language))   
        #elif language == 'greek':
        #    os.system('python3 /srv/bridge-repo/lemmatizer/convert_lemmata_format.py {0} import /srv/bridge-repo/lemmatizer/Convert-bridge-morpheus-greek.xlsx'.format(language))   

        new_filename = filename.split('.')[0] + '.xlsx'
        if format == 'bridge':
            os.system('python3 /srv/bridge-repo/lemmatizer/convert_lemmata_format.py {0} convert {1} morpheus bridge'.format(language,new_filename))
            #os.system('python3 /srv/bridge-repo/lemmatizer/format_lemmatized_text.py {0}'.format(new_filename))

        else:
            pass
         
    except:
        print ('Unable to lemmatize file.')   


        #Output is a file with filename_Input.xlsx 


#lemmatize('greek','greek_text.txt','bridge')
def format(filename):
    try:
        os.system('python3 /srv/bridge-repo/lemmatizer/format_lemmatized_text.py {0}'.format(filename))
    except:
        print ('Unable to format lemmatized file.')
