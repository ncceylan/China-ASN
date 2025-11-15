#!/bin/sh

# 函数定义
download_and_create_filter() {
    local file_name="$1"
    local list_name="$2"
    local url="$3"
    local output_file="$4"

    echo "Downloading ${file_name} from ${url}..."
    wget --no-check-certificate -c -O "$file_name" "$url"

    {
        echo "/routing filter num-list"

        while read -r net; do
            if [ -n "$net" ]; then
                echo "add list=$list_name range=$net"
            fi
        done < "$file_name"

    } > "$output_file"

    echo "${file_name} processing completed. Output: ${output_file}"
}

# 主程序
echo "🏗️ 开始构建PBR规则..."
echo "📍 当前目录: $(pwd)"

# 确保ASN文件存在
for file in asn_cn.conf asn_ct.conf asn_cmcc.conf; do
    if [ ! -f "$file" ]; then
        echo "❌ 错误: $file 不存在，请先运行ASN更新工作流"
        exit 1
    fi
done

output_directory="./pbr"
mkdir -p "${output_directory}"
cd "${output_directory}" || exit 1

# 使用本地的ASN文件
echo "📋 使用本地ASN文件..."

# CN (从本地文件)
cp ../asn_cn.conf CN.txt
{
    echo "/routing filter num-list"
    while read -r net; do
        if [ -n "$net" ]; then
            echo "add list=CN range=$net"
        fi
    done < "CN.txt"
} > "../CN.rsc"
echo "CN.rsc 生成完成"

# CMCC (从本地文件)  
cp ../asn_cmcc.conf CMCC.txt
{
    echo "/routing filter num-list"
    while read -r net; do
        if [ -n "$net" ]; then
            echo "add list=CMCC range=$net"
        fi
    done < "CMCC.txt"
} > "../CMCC.rsc"
echo "CMCC.rsc 生成完成"

# CT (从本地文件)
cp ../asn_ct.conf CT.txt
{
    echo "/routing filter num-list"
    while read -r net; do
        if [ -n "$net" ]; then
            echo "add list=CT range=$net"
        fi
    done < "CT.txt"
} > "../CT.rsc"
echo "CT.rsc 生成完成"

cd ..
rm -rf "${output_directory}"
echo "🎉 PBR构建完成!"
