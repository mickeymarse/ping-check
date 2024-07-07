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
    sites = ['https://tarmarapi.fly.dev/', 'https://metrakapi.fly.dev/', 'https://mickeymarse.dev/', 'https://21-sid-website.vercel.app/']
    data_list = []

    for site in sites:
        try:
            session = requests.Session()
            session.headers['User-Agent'] = USER_AGENT
            session.headers['Accept-Language'] = LANGUAGE
            session.headers['Content-Language'] = LANGUAGE
            r = session.get(f'{site}')
            html_content = r.text
            status = r.status_code
            soup = BeautifulSoup(html_content, 'html.parser')
            data = dict()
            id = site.split('//')[1].split('.')[0][:2]
            data['id'] = id
            data['site'] = site
            data['title'] = soup.find('title').text if soup.find('title') else None
            data['status'] = status
            data['element'] = soup.find('h1').text if soup.find('h1') else soup.find('p').text
            data_list.append(data)
            print(data_list)
        except requests.exceptions.ConnectionError as e:
            print(f"ConnectionError occurred for site: {site}")
            id = site.split('//')[1].split('.')[0][:2]
            status = r.status_code if 'r' in locals() else 0
            data = {'id': id, 'site': site, 'title': None, 'status': status, 'element': None}
            data_list.append(data)
            print(data_list)
        except Exception as e:
            print(f"Exception occurred for site: {site}")
            id = site.split('//')[1].split('.')[0][:2]
            status = r.status_code if 'r' in locals() else 500
            data = {'id': id, 'site': site, 'title': None, 'status': status, 'element': None}
            data_list.append(data)
            print(data_list)

    return data_list

def home(request):
    try:
        data_list = automated_get_request()
        return render(request, 'core/home.html', {'data_list': data_list})
    except Exception as e:
        error_message = "An unexpected error occurred. Please try again later."
        return render(request, 'error_template.html', {'error_message': error_message})

def start_automated_get_request():
    interval = getattr(settings, 'AUTOMATED_GET_REQUEST_INTERVAL', 300)
    while True:
        automated_get_request()
        time.sleep(interval)

threading.Thread(target=start_automated_get_request, daemon=True).start()
