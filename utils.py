from bs4 import BeautifulSoup
from constants import ELEM_TYPE

import requests

def is_good_response(res):
    if res is None:
        print('Response is invalid')
        return False
    else:
        return True

def request_data(url):
    try:
        data = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    if is_good_response(data):
        return data.content
    else:
        return None

def get_elem_by_type(url):
    raw_html = open(url).read()
    html = BeautifulSoup(raw_html, 'html.parser')
    html_content_dict = {}

    if html is None:
        return 'Error: No elements could be read'

    for e in ELEM_TYPE:
        elem = html.select(e)

        if len(elem) != 0 or None:
            html_content_dict[f'{e}'] = elem

    return html_content_dict
