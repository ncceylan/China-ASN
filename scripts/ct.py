import re
import os
import requests
from proxy_helper import get_free_proxies, get_random_proxy

def get_last_line(file_name):
    with open(file_name, 'rb') as f:
        file_size = os.path.getsize(file_name)
        offset = -100
        if file_size == 0:
            return ''
        while True:
            if abs(offset) >= file_size:
                f.seek(-file_size, 2)
                data1 = f.readlines()
                return data1[-1]
            f.seek(offset, 2)
            data1 = f.readlines()
            if len(data1) > 1:
                return data1[-1]
            else:
                offset *= 2

file_name = '../asn_ct.conf'
datas_source = 'https://whois.ipip.net/search/CHINA%20TELECOM'

proxies = get_free_proxies()
proxy = get_random_proxy(proxies)

proxy_dict = {
    'http': f'http://{proxy}',
    'https': f'http://{proxy}',  # 注意，这里也使用了HTTP代理，因为免费代理可能不支持HTTPS
}
response = requests.get(datas_source, proxies=proxy_dict)
html = response.text

with open(file_name, 'w') as file:
    file.write('define ct_asn = [\n')

results = re.findall(', CN\">AS(.*?)</a> </td>', html, re.S)
for result in results[:-1]:
    with open(file_name, 'a') as file_object:
        str2 = result.strip() + ',\n'
        file_object.write(str2)

last_result = results[-1]
with open(file_name, 'a') as file_object:
    str2 = last_result.strip() + '\n];\n'
    file_object.write(str2)

print("生成中国电信ASN成功!")
