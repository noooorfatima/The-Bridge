import os
import subprocess
path = os.path.dirname(os.path.realpath(__file__))
import sys

def lemmatize(language,filename,format,lem_level):
    try:

        if lem_level == 'Ambiguous':
            key = '-a'
        else:
            key = ''
        if format == 'bridge':
            ui = '--force-ui'
        else:
            ui = ''
        #subprocess.call('python3 /srv/bridge3/lemmatizer/autoLemma.py {0} {1}'.format(language, filename), shell=False)
        #os.system('pip3 install cltk')
        print(sys.path, 'sys path')
        os.system('python3 /srv/bridge3/lemmatizer/autoLemma.py {0} --force-no-punctuation {1} {2} {3}'.format(language, ui, key, filename))
        #subprocess.Popen(["/srv/bridge3_env/bin/python3", "/srv/bridge3/lemmatizer/autoLemma.py {0} --force-no-punctuation {1} {2} {3}".format(language,ui, key, filename)])
        #convert lemma format to Bridge
        #if language == 'latin':
        #    os.system('python3 /srv/bridge3/lemmatizer/convert_lemmata_format.py {0} import /srv/bridge3/lemmatizer/morpheus-bridge.xlsx'.format(language))
        #elif language == 'greek':
        #    os.system('python3 /srv/bridge3/lemmatizer/convert_lemmata_format.py {0} import /srv/bridge3/lemmatizer/Convert-bridge-morpheus-greek.xlsx'.format(language))

        new_filename = filename.split('.')[0] + '.xlsx'
        if format == 'bridge':
            os.system('python3 /srv/bridge3/lemmatizer/convert_lemmata_format.py {0} convert {1} morpheus bridge'.format(language,new_filename))
            #os.system('python3 /srv/bridge3/lemmatizer/format_lemmatized_text.py {0}'.format(new_filename))

        else:
            pass

    except Exception as e:
        print('ERROR', e)
        print ('Unable to lemmatize file.')


        #Output is a file with filename_Input.xlsx


#lemmatize('greek','greek_text.txt','bridge')
def format(filename):
    try:
        os.system('python3 /srv/bridge3/lemmatizer/format_lemmatized_text.py {0}'.format(filename))
    except:
        print ('Unable to format lemmatized file.')
