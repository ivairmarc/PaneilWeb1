"""To render html web page"""
from django.http import HttpResponse
import sys
import requests
from http.client import responses
import validators
import pandas as pd
import os
import time
import PySimpleGUI as sg

caminho = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(caminho)
caminho_Arquivo = 'urls.xlsx'


HTML_STRING = """
<h1>Helo</h1>

"""


def home(request):

    """"Take in a request 
        Return HTML as a response (We pick to return the response)"""
    return HttpResponse(HTML_STRING)


