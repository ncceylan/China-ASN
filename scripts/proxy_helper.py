# proxy_helper.py
import requests
import random

def get_free_proxies():
    proxy_api = 'https://www.proxy-list.download/api/v1/get?type=http'
    response = requests.get(proxy_api)
    proxies = response.text.split('\r\n')
    return proxies[:-1]

def get_random_proxy(proxies):
    return random.choice(proxies)
