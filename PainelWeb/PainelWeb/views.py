"""To render html web page"""
from django.http import HttpResponse

HTML_STRING = """
<h1>Helo</h1>

"""


def home(request):

    """"Take in a request 
        Return HTML as a response (We pick to return the response)"""
    return HttpResponse(HTML_STRING)