#!/srv/bridge3_env/bin/python3.5
import cgitb
cgitb.enable()
def getData():
    formData = cgi.FieldStorage() #note that FieldStorage is a class, and is very simimlar to a dictionary
    language = formData.getvalue('language')
    textlist = formData.getlist("textlsit")
    text_from =formData.getlist('text_from')
    text_to =formData.getlist('text_to')
    #those two are for the main text
    text_ranges = []
    for text in textlist:
        text_ranges.append(formData.getvalue(text))
    return {'textlist' : textlist, 'language' : language, 'text_from' : text_from, 'text_to' : text_to, 'text_ranges' : text_ranges}

if __name__ == "__main__":
    cgi.print_environ(language, textlist, text_from, text_to, text_ranges)
    return getData
