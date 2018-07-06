from django.test import TestCase
from new_bridge import *

class ViewsTestCase(TestCase):
    """ViewsTestCase: tests for views.py"""
    def setUp(self):
        #what ever i need to do to set up tests goes here... not sure what i need yet though
        self.factory = RequestFactory()

    def index_test(self):
        request = self.factory.get("/")
        response = IndexView(request)

    def words_page_test(self):
        request = self.factory.post("")
