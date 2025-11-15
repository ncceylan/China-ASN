import requests
from bs4 import BeautifulSoup
import re
import os
import sys

def get_asn_from_url(url):
    """从URL获取ASN号码"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, timeout=30, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        asn_tags = soup.find_all('a', string=re.compile(r'AS\d+'))
        
        asn_numbers = list(set(tag.string[2:] for tag in asn_tags))
        return sorted(asn_numbers, key=int)
        
    except Exception as e:
        print(f"❌ 请求失败 {url}: {e}")
        return None

def save_asn_to_file(asn_numbers, filename):
    """保存ASN号码到文件（根目录）"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('\n'.join(asn_numbers))
        print(f"✅ 成功保存 {filename} ({len(asn_numbers)}个ASN)")
        return True
    except Exception as e:
        print(f"❌ 文件保存失败 {filename}: {e}")
        return False

def remove_duplicate_asns(file_a, file_b):
    """移除文件A中与文件B重复的ASN"""
    try:
        if not os.path.exists(file_a):
            print(f"⚠️ 文件 {file_a} 不存在")
            return False
            
        if not os.path.exists(file_b):
            print(f"⚠️ 文件 {file_b} 不存在，跳过去重")
            return False
            
        with open(file_a, 'r') as file:
            asns_a = set(line.strip() for line in file if line.strip())
        
        with open(file_b, 'r') as file:
            asns_b = set(line.strip() for line in file if line.strip())
        
        asns_to_keep = asns_a - asns_b
        
        removed_count = len(asns_a) - len(asns_to_keep)
        print(f"📊 从 {file_a} 中移除 {removed_count} 个重复ASN")
        
        with open(file_a, 'w') as file:
            file.write('\n'.join(sorted(asns_to_keep, key=int)))
        
        return True
        
    except Exception as e:
        print(f"❌ 处理文件时出错: {e}")
        return False

def main():
    # 获取当前工作目录（main分支根目录）
    current_dir = os.getcwd()
    print(f"📍 工作目录: {current_dir}")
    
    # 目标URL和对应文件名
    urls = [
        ('http://whois.ipip.net/countries/CN', 'asn_cn.conf'),
        ('http://whois.ipip.net/search/CHINA%20TELECOM', 'asn_ct.conf'),
        ('http://whois.ipip.net/search/CHINA%20MOBILE', 'asn_cmcc.conf')
    ]
    
    print("🚀 开始获取ASN数据...")
    
    # 收集所有ASN数据
    success_count = 0
    for url, filename in urls:
        print(f"📡 正在获取 {url} ...")
        asn_numbers = get_asn_from_url(url)
        
        if asn_numbers:
            if save_asn_to_file(asn_numbers, filename):
                success_count += 1
            else:
                print(f"❌ 生成 {filename} 失败")
        else:
            print(f"❌ 未能获取 {filename} 数据")
    
    # 执行去重操作（仅当所有文件都成功生成时）
    if success_count == len(urls):
        print("🔄 执行去重操作...")
        if remove_duplicate_asns('asn_cn.conf', 'asn_cmcc.conf'):
            print("✅ 去重操作完成")
        else:
            print("⚠️ 去重操作出现问题")
    else:
        print("⚠️ 由于部分数据获取失败，跳过去重操作")
    
    # 最终文件统计
    print("\n📊 最终文件统计:")
    total_asns = 0
    for filename in ['asn_cn.conf', 'asn_ct.conf', 'asn_cmcc.conf']:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
                count = len(lines)
                total_asns += count
                print(f"  📄 {filename}: {count}个ASN")
        else:
            print(f"  ❌ {filename}: 文件不存在")
    
    print(f"📈 总共生成: {total_asns}个ASN")
    
    # 设置退出码
    sys.exit(0 if success_count > 0 else 1)

if __name__ == "__main__":
    main()
