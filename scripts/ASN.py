import requests
from bs4 import BeautifulSoup

def get_asn_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        asn_tags = soup.find_all('a', string=re.compile(r'AS\d+'))
        return [tag.string[2:] for tag in asn_tags]
    else:
        return None

def save_asn_to_file(asn_numbers, file_name):
    file_path = '/home/' + file_name  # 拼接完整的文件路径
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(asn_numbers))

def remove_duplicate_asns(file_a, file_b):
    file_path_a = '/home/' + file_a  # 拼接完整的文件路径
    file_path_b = '/home/' + file_b  # 拼接完整的文件路径

    with open(file_path_a, 'r') as file_a:
        asns_a = set(file_a.read().splitlines())

    with open(file_path_b, 'r') as file_b:
        asns_b = set(file_b.read().splitlines())

    # Find ASNs in file_a that are not in file_b
    asns_to_remove = asns_a.difference(asns_b)

    # Save the updated file_a, including only ASNs not in file_b
    with open(file_path_a, 'w') as file_a:
        file_a.write('\n'.join(asns_to_remove))

def main():
    urls = [
        ('http://whois.ipip.net/countries/CN', 'asn_cn.conf'),
        ('http://whois.ipip.net/search/CHINA%20TELECOM', 'asn_ct.conf'),
        ('http://whois.ipip.net/search/CHINA%20MOBILE', 'asn_cmcc.conf')
    ]

    for url, file_name in urls:
        asn_numbers = get_asn_from_url(url)

        if asn_numbers is not None:
            save_asn_to_file(asn_numbers, file_name)
            print(f"生成 {file_name} 成功!")
        else:
            print(f"未能获取 {file_name} 数据。请检查网络连接或数据源.")

    # Remove duplicate ASNs in asn_cn.conf
    remove_duplicate_asns('asn_cn.conf', 'asn_cmcc.conf')

if __name__ == "__main__":
    main()
