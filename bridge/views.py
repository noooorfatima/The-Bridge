from django.views import generic
from new_bridge.models import BookTable, WordTable, BookTitles, BookTableGreek, WordTableGreek, BookTitlesGreek
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response

