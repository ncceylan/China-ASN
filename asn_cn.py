# version :Python 3.7.3
import os
import re
import urllib.request


# 读出文件最后一行
# 参考大神代码https://blog.csdn.net/weixin_30632899/article/details/97566294
def getEndLing(name):
    with open(name, 'rb') as f:
        file_size = os.path.getsize(name)
        offset = -100
        # 文件字节大小为0则返回none
        if file_size == 0:
            return ''
        while True:
            # 判断offset是否大于文件字节数,是则读取所有行，并返回最后一行
            if abs(offset) >= file_size:
                f.seek(-file_size, 2)
                data1 = f.readlines()
                return data1[-1]
            # 游标移动倒数的字节数位置
            f.seek(offset, 2)
            data1 = f.readlines()
            # 判断读取到的行数，如果大于1则返回最后一行，否则扩大offset
            if len(data1) > 1:
                return data1[-1]
            else:
                offset *= 2

file_name = 'asn_cn.conf'
str1 = 'define china_asn = ['
str5 = '];'
datas_source = 'https://whois.ipip.net/countries/CN'

response = urllib.request.urlopen(datas_source)

html = response.read().decode('utf-8')

with open(file_name, 'a') as file:
    file.write(str1 + "\n")
print("step 1.添加文件第一行字符串!")

results = re.findall(', CN\">AS(.*?)</a> </td>', html, re.S)
for result in results:
    with open(file_name, 'a') as file_object:
        str2 = result.strip() + ',' + '\n'
        file_object.write(str2)
print("step 2.采集ASN号数据!")

data2 = getEndLing(file_name)
if data2:
    str3 = data2.decode('utf-8').strip()


with open(file_name,"r",encoding="utf-8") as f:
    lines = f.readlines()
    #print(lines)
with open(file_name,"w",encoding="utf-8") as f_w:
    for line in lines:
        if str3 in line:
            continue
        f_w.write(line)
print("step 3.提取数据完成!")

str4 = str3[:-1]
with open(file_name, 'a') as file:
    file.write(str4 + "\n")
    file.write(str5)

print("step 4.生成中国区ASN成功!")
