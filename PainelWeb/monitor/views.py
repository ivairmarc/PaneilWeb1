from django.shortcuts import render, redirect
import requests
import time
import psutil
import os
from datetime import datetime
from .models import Monitor
from urllib.parse import urlparse
from django.core.paginator import Paginator

import sys
import requests
from http.client import responses
import validators
import pandas as pd
import os
import time
import PySimpleGUI as sg

caminho = os.path.abspath(os.path.dirname(sys.argv[0]))

caminho_Arquivo = f'{caminho}\\urls.xlsx'

#traffic monitor
def traffic_monitor(request):
    dataSaved = Monitor.objects.all().order_by('-datetime')
    # Getting loadover15 minutes 
    load1, load5, load15 = psutil.getloadavg()
    cpu_usage = int((load15/os.cpu_count()) * 100)
    ram_usage = int(psutil.virtual_memory()[2])
    p = Paginator(dataSaved, 100)
    #shows number of items in page
    totalSiteVisits = (p.count)
    #find unique page viewers & Duration
    pageNum = request.GET.get('page', 1)
    page1 = p.page(pageNum)
    #unique page viewers
    a = Monitor.objects.order_by().values('ip').distinct()
    pp = Paginator(a, 10)
    #shows number of items in page
    unique = (pp.count)
    #update time
    now = datetime.now()
    data = {
        "now":now,
        "unique":unique,
        "totalSiteVisits":totalSiteVisits,
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage,
        "dataSaved": page1,
    }

    consulta = pd.read_excel(caminho_Arquivo)
    consulta_livre = consulta[(consulta['STATUS'].isnull())]

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    erro = ''
    for ind_base, linha2 in consulta_livre.iterrows():
        ######## CONSULTA
        Url = linha2["ISSWEB"]
        country = linha2['MUNICIPIO']
    
        print(f"{country}\n")
        try:
            #for i in range(1, n):
            url = Url #sys.argv[i]
            if validators.url(url) is True:
                status = requests.head(url).status_code
                try:
                    print(url, status,responses[status], "\n")

                except:
                    print(url, status, "Not an Standard HTTP Response code\n")
                    sg.popup_error(f'{status}')
            else:
                print(url, "Not an valid URL\n")
                continue
            time.sleep(1)
        except Exception as er:
            sg.popup_error('Site Off')
            erro = 'Site Off'
            print(f'Uma tentativa de conexão falhou porque o componente conectado não respondeu corretamente após um período de tempo ou a conexão estabelecida falhou porque o host conectado não respondeu')
        
        now = datetime.now()
        datetimenow = now.strftime("%Y-%m-%d")
        saveNow = Monitor(
        continent=status,
        country=country,
        capital='capital',
        city=erro,
        datetime=datetimenow,
        ip=url
        )
        saveNow.save()
    return render(request, 'traffic_monitor.html', data)






#home page
def home(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    response = requests.get('http://api.ipstack.com/'+ip+'?access_key=') # fc450529e6c1bd0d4a42eb38928627e7 change from HTTP to HTTPS on the IPSTACK API if you have a premium account
    rawData = response.json()
    print(rawData) # print this out to look at the response
    continent = rawData['continent_name']
    country = rawData['country_name']
    capital = rawData['city']
    city = rawData['location']['capital']
    now = datetime.now()
    datetimenow = now.strftime("%Y-%m-%d")
    saveNow = Monitor(
        continent=continent,
        country=country,
        capital=capital,
        city=city,
        datetime=datetimenow,
        ip=ip
    )
    saveNow.save()
    return render(request, 'home.html')


def main(request):
    consulta = pd.read_excel(caminho_Arquivo)
    consulta_livre = consulta[(consulta['STATUS'].isnull())]

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
                
    for ind_base, linha2 in consulta_livre.iterrows():
        ######## CONSULTA
        Url = linha2["ISSWEB"]
        country = linha2['MUNICIPIO']
    
        print(f"{country}\n")
        try:
            #for i in range(1, n):
            url = Url #sys.argv[i]
            if validators.url(url) is True:
                status = requests.head(url).status_code
                try:
                    print(url, status,responses[status], "\n")

                except:
                    print(url, status, "Not an Standard HTTP Response code\n")
                    sg.popup_error(f'{status}')
            else:
                print(url, "Not an valid URL\n")
                continue
            time.sleep(1)
        except Exception as er:
            sg.popup_error('Site Off')
            print(f'Uma tentativa de conexão falhou porque o componente conectado não respondeu corretamente após um período de tempo ou a conexão estabelecida falhou porque o host conectado não respondeu')
        
        now = datetime.now()
        datetimenow = now.strftime("%Y-%m-%d")
        saveNow = Monitor(
        continent=status,
        country=country,
        capital='capital',
        city=country,
        datetime=datetimenow,
        ip=url
        )
        saveNow.save()
    return render(request, 'home.html')
    
    """time.sleep(1000)
    main()"""
    