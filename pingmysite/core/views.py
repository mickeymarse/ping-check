from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def get_r(site):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    site = site.replace(' ', '+')
    r = session.get(f'{site}')
    return r


def home(request):
    data = None
    if 'site' in request.GET:
        # fetch
        site = request.GET.get('site')
        r = get_r(site)
        html_content = r.text
        status = r.status_code
        soup = BeautifulSoup(html_content, 'html.parser')
        data = dict()
        data['status'] = status
        data['heading'] = soup.find('h1').text
        print(f'{data}')
    return render(request, 'core/home.html', {'data': data})
