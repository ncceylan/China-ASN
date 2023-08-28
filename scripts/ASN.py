import re
import requests


def get_asn_from_url(url, file_name):
    response = requests.get(url)
    html = response.text

    results = re.findall(r'<a href="/as/(\d+)"', html)
    if not results:
        print(f"未能获取 {file_name} 数据。请检查网络连接或数据源。")
        return

    with open(file_name, 'w', encoding='utf-8') as file:
        for result in results[:-1]:
            file.write(result.strip() + '\n')
        file.write(results[-1].strip())

    print(f"生成 {file_name} 成功!")


def main():
    get_asn_from_url('https://bgp.he.net/country/CN', 'asn_cn.conf')
    get_asn_from_url('https://bgp.he.net/search?search%5Bsearch%5D=CHINA+TELECOM&type=IPv4', 'asn_ct.conf')
    get_asn_from_url('https://bgp.he.net/search?search%5Bsearch%5D=CHINA+MOBILE&type=IPv4', 'asn_cmcc.conf')


if __name__ == "__main__":
    main()
