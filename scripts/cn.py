import os
import re
import requests

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

file_name = '../asn_cn.conf'
datas_source = 'https://whois.ipip.net/countries/CN'

response = requests.get(datas_source)
html = response.text

with open(file_name, 'w') as file:
    file.write('define china_asn = [\n')

results = re.findall(', CN\">AS(.*?)</a> </td>', html, re.S)
for result in results[:-1]:
    with open(file_name, 'a') as file_object:
        str2 = result.strip() + ',\n'
        file_object.write(str2)

last_result = results[-1]
with open(file_name, 'a') as file_object:
    str2 = last_result.strip() + '\n];\n'
    file_object.write(str2)

print("生成中国区ASN成功!")
