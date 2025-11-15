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

def save_asn_to_file(asn_numbers, file_path):
    """保存ASN号码到文件"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(asn_numbers))
        return True
    except Exception as e:
        print(f"❌ 文件保存失败 {file_path}: {e}")
        return False

def remove_duplicate_asns(file_path_a, file_path_b):
    """移除文件A中与文件B重复的ASN"""
    try:
        if not os.path.exists(file_path_a):
            print(f"⚠️  文件 {file_path_a} 不存在")
            return False
            
        if not os.path.exists(file_path_b):
            print(f"⚠️  文件 {file_path_b} 不存在，跳过去重")
            return False
            
        with open(file_path_a, 'r') as file:
            asns_a = set(line.strip() for line in file if line.strip())
        
        with open(file_path_b, 'r') as file:
            asns_b = set(line.strip() for line in file if line.strip())
        
        asns_to_keep = asns_a - asns_b
        
        removed_count = len(asns_a) - len(asns_to_keep)
        print(f"📊 从 {os.path.basename(file_path_a)} 中移除 {removed_count} 个重复ASN")
        
        with open(file_path_a, 'w') as file:
            file.write('\n'.join(sorted(asns_to_keep, key=int)))
        
        return True
        
    except Exception as e:
        print(f"❌ 处理文件时出错: {e}")
        return False

def main():
    # 使用当前目录（main分支根目录）
    output_dir = os.getcwd()
    print(f"📁 输出目录: {output_dir}")
    
    urls = [
        ('http://whois.ipip.net/countries/CN', 'asn_cn.conf'),
        ('http://whois.ipip.net/search/CHINA%20TELECOM', 'asn_ct.conf'),
        ('http://whois.ipip.net/search/CHINA%20MOBILE', 'asn_cmcc.conf')
    ]
    
    print("🚀 开始获取ASN数据...")
    
    # 收集所有ASN数据
    success_count = 0
    for url, file_name in urls:
        print(f"📡 正在获取 {url} ...")
        asn_numbers = get_asn_from_url(url)
        
        if asn_numbers:
            # 直接保存到当前目录（main根目录）
            file_path = os.path.join(output_dir, file_name)
            if save_asn_to_file(asn_numbers, file_path):
                print(f"✅ 成功生成 {file_name} ({len(asn_numbers)}个ASN)")
                success_count += 1
            else:
                print(f"❌ 生成 {file_name} 失败")
        else:
            print(f"❌ 未能获取 {file_name} 数据")
    
    # 执行去重操作
    if success_count == len(urls):
        print("🔄 执行去重操作...")
        cn_file = os.path.join(output_dir, 'asn_cn.conf')
        cmcc_file = os.path.join(output_dir, 'asn_cmcc.conf')
        
        if remove_duplicate_asns(cn_file, cmcc_file):
            print("✅ 去重操作完成")
        else:
            print("⚠️ 去重操作出现问题")
    else:
        print("⚠️ 由于部分数据获取失败，跳过去重操作")
    
    # 输出文件列表
    print("\n📁 生成的文件:")
    for file_name in ['asn_cn.conf', 'asn_ct.conf', 'asn_cmcc.conf']:
        file_path = os.path.join(output_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                line_count = len([line for line in f if line.strip()])
            print(f"  📄 {file_name}: {line_count}个ASN")
        else:
            print(f"  ❌ {file_name}: 文件不存在")
    
    # 设置退出码
    if success_count == len(urls):
        print("🎉 所有任务完成!")
        sys.exit(0)
    else:
        print("💥 部分任务失败!")
        sys.exit(1)

if __name__ == "__main__":
    main()
