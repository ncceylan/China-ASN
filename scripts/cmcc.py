import os
import re
import requests


def get_last_line(file_name):
    with open(file_name, 'rb') as f:
        file_size = os.path.getsize(file_name)
        offset = -100
        while True:
            if abs(offset) >= file_size:
                f.seek(-file_size, 2)
                lines = f.readlines()
                return lines[-1]
            f.seek(offset, 2)
            lines = f.readlines()
            if len(lines) > 1:
                return lines[-1]
            else:
                offset *= 2


def main():
    file_name = '../asn_cmcc.conf'
    datas_source = 'https://whois.ipip.net/search/CHINA%20MOBILE'

    response = requests.get(datas_source)
    html = response.text

    results = re.findall(', CN\">AS(.*?)</a> </td>', html, re.S)
    if not results:
        print("未能获取 ASN 数据。请检查网络连接或数据源。")
        return

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write('define china_asn = [\n')
        for result in results[:-1]:
            file.write(f"{result.strip()},\n")
        file.write(f"{results[-1].strip()}\n];\n")

    print("生成中国移动ASN成功!")


if __name__ == "__main__":
    main()
