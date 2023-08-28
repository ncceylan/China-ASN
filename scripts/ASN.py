import requests
from bs4 import BeautifulSoup

def get_html_content(url):
    response = requests.get(url)
    return response.text

def extract_asn_numbers(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    asn_tags = soup.find_all('a', string=re.compile(r'AS\d+'))
    return [tag.string[2:] for tag in asn_tags]

def save_asn_to_file(asn_numbers, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write('\n'.join(asn_numbers))

def main():
    urls = [
        ('https://whois.ipip.net/countries/CN', 'asn_cn.conf'),
        ('https://whois.ipip.net/search/CHINA%20TELECOM', 'asn_ct.conf'),
        ('https://whois.ipip.net/search/CHINA%20MOBILE', 'asn_cmcc.conf')
    ]

    for url, file_name in urls:
        html_content = get_html_content(url)
        asn_numbers = extract_asn_numbers(html_content)

        if not asn_numbers:
            print(f"未能获取 {file_name} 数据。请检查网络连接或数据源。")
        else:
            save_asn_to_file(asn_numbers, file_name)
            print(f"生成 {file_name} 成功!")

if __name__ == "__main__":
    main()
