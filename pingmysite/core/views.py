# from django.shortcuts import render
# import requests
# from bs4 import BeautifulSoup

# def get_r(site):
#     USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
#     LANGUAGE = "en-US,en;q=0.5"
#     session = requests.Session()
#     session.headers['User-Agent'] = USER_AGENT
#     session.headers['Accept-Language'] = LANGUAGE
#     session.headers['Content-Language'] = LANGUAGE
#     site = site.replace(' ', '+')
#     r = session.get(f'{site}')
#     return r


# def home(request):
#     data = None
#     if 'site' in request.GET:
#         # fetch
#         site = request.GET.get('site')
#         r = get_r(site)
#         html_content = r.text
#         status = r.status_code
#         soup = BeautifulSoup(html_content, 'html.parser')
#         data = dict()
#         data['status'] = status
#         data['heading'] = soup.find('h1').text
#         print(f'{data}')
#     return render(request, 'core/home.html', {'data': data})

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.conf import settings
from django.utils.timezone import now
import threading
import time

def automated_get_request():
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    sites = ['https://tarmarapi.fly.dev/', 'https://metrak.fly.dev/', 'https://mickeymarse.dev/']
    data_list = []

    for site in sites:
        session = requests.Session()
        session.headers['User-Agent'] = USER_AGENT
        session.headers['Accept-Language'] = LANGUAGE
        session.headers['Content-Language'] = LANGUAGE
        r = session.get(f'{site}')
        html_content = r.text
        status = r.status_code
        soup = BeautifulSoup(html_content, 'html.parser')
        data = dict()
        data['title'] = soup.find('title').text if soup.find('title') else None
        data['status'] = status
        data['element'] = soup.find('p').text if soup.find('p') else None
        data_list.append(data)
        print(data_list)

    return data_list

def home(request):
    data_list = automated_get_request()
    return render(request, 'core/home.html', {'data_list': data_list})


def start_automated_get_request():
    interval = getattr(settings, 'AUTOMATED_GET_REQUEST_INTERVAL', 10)
    while True:
        automated_get_request()
        time.sleep(interval)

# Start the automated GET request in a separate thread
threading.Thread(target=start_automated_get_request, daemon=True).start()

