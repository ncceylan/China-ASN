import re
import requests


def get_asn_from_url(url, file_name):
    response = requests.get(url)
    html = response.text

    results = re.findall(', CN\">AS(.*?)</a> </td>', html, re.S)
    if not results:
        print(f"未能获取 {file_name} 数据。请检查网络连接或数据源。")
        return

    with open(file_name, 'w', encoding='utf-8') as file:
        for result in results[:-1]:
            file.write(result.strip() + '\n')
        file.write(results[-1].strip())

    print(f"生成 {file_name} 成功!")


def main():
    get_asn_from_url('https://whois.ipip.net/countries/CN', 'asn_cn.conf')
    get_asn_from_url('https://whois.ipip.net/search/CHINA%20TELECOM', 'asn_ct.conf')
    get_asn_from_url('https://whois.ipip.net/search/CHINA%20MOBILE', 'asn_cmcc.conf')


if __name__ == "__main__":
    main()
