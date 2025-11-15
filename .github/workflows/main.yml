# scripts/ASN.py
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
        print(f"🌐 请求URL: {url}")
        response = requests.get(url, timeout=30, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        asn_tags = soup.find_all('a', string=re.compile(r'AS\d+'))
        
        print(f"🔍 找到 {len(asn_tags)} 个ASN标签")
        asn_numbers = list(set(tag.string[2:] for tag in asn_tags if tag.string))
        print(f"📊 去重后获得 {len(asn_numbers)} 个ASN号码")
        
        return sorted(asn_numbers, key=int)
        
    except Exception as e:
        print(f"❌ 请求失败 {url}: {e}")
        return None

def main():
    # 详细的路径调试
    current_dir = os.getcwd()
    print(f"📍 当前工作目录: {current_dir}")
    print(f"📁 目录内容: {os.listdir('.')}")
    
    # 检查脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"📜 脚本目录: {script_dir}")
    
    urls = [
        ('http://whois.ipip.net/countries/CN', 'asn_cn.conf'),
        ('http://whois.ipip.net/search/CHINA%20TELECOM', 'asn_ct.conf'),
        ('http://whois.ipip.net/search/CHINA%20MOBILE', 'asn_cmcc.conf')
    ]
    
    print("🚀 开始获取ASN数据...")
    
    for url, filename in urls:
        print(f"\n📡 处理 {filename} ...")
        asn_numbers = get_asn_from_url(url)
        
        if asn_numbers:
            file_path = os.path.join(current_dir, filename)
            print(f"💾 保存路径: {file_path}")
            
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write('\n'.join(asn_numbers))
                print(f"✅ 成功保存 {filename}")
                
                # 确认文件已创建
                if os.path.exists(filename):
                    file_size = os.path.getsize(filename)
                    print(f"📏 文件大小: {file_size} 字节")
                else:
                    print("❌ 文件创建失败")
                    
            except Exception as e:
                print(f"❌ 保存失败: {e}")
        else:
            print(f"❌ 未能获取 {filename} 数据")
    
    # 最终检查
    print(f"\n🔍 最终目录内容:")
    for item in os.listdir('.'):
        if item.endswith('.conf'):
            size = os.path.getsize(item)
            print(f"  📄 {item}: {size} 字节")

if __name__ == "__main__":
    main()
