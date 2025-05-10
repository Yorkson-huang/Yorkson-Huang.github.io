import urllib.request, urllib.error
import re
import json
import os
import sys
from datetime import datetime

def get_references(title):
    """获取论文的引用计数"""
    print(f"正在获取论文引用数: {title}")
    # 将文章标题中的空格替换为加号，以便用于生成 URL
    title = title.replace(' ', '+')

    # 构造搜索 URL
    search_url = f'https://scholar.google.com/scholar?hl=en&q={title}&btnG=&as_sdt=1%2C5&as_sdtp='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.google.com/'
    }
    # 发送 HTTP 请求并读取响应内容
    req = urllib.request.Request(search_url, headers=headers)
    try:
        response = urllib.request.urlopen(req)
        html_content = response.read().decode('utf-8')
        print(f"成功获取搜索结果，内容长度: {len(html_content)} 字符")
    except urllib.error.HTTPError as e:
        print(f'Error: {e.code} {e.reason}')
        return 0
    except Exception as e:
        print(f"获取搜索结果时出错: {str(e)}")
        return 0

    # 从 HTML 页面中提取被引用次数
    m = re.search('Cited by\s(\d+)', html_content)
    if m:
        num_citations = int(m.group(1))
        print(f"找到引用数: {num_citations}")
        return num_citations
    else:
        print("未找到引用数，返回0")
        return 0

def main():
    print(f"开始运行脚本，Python版本: {sys.version}")
    print(f"当前工作目录: {os.getcwd()}")
    
    # 论文标题和ID
    papers = [
        {
            'title': 'Sentiment Analysis Using E-Commerce Review Keyword-Generated Image with a Hybrid Machine Learning-Based Model',
            'id': 'edyJPQQAAAAJ:d1gkVwhDpl0C'
        },
        {
            'title': 'An Improved Hybrid CNN-LSTM-Attention Model with Kepler Optimization Algorithm for Wind Speed Prediction',
            'id': 'edyJPQQAAAAJ:2osOgNQ5qMEC'
        },
        {
            'title': 'A FinBERT Framework for Sentiment Analysis of Chinese Financial News',
            'id': 'edyJPQQAAAAJ:ufrVoPGSRksC'
        },
        {
            'title': 'An Ensemble Learning Approach for Wind Power Forecasting',
            'id': 'edyJPQQAAAAJ:9yKSN-GCB0IC'
        }
    ]
    
    # 获取每篇论文的引用数
    total_citations = 0
    for paper in papers:
        try:
            citations = get_references(paper['title'])
            paper['num_citations'] = citations
            total_citations += citations
            print(f"{paper['title']}: {citations} 次被引用")
        except Exception as e:
            print(f"处理论文时出错: {str(e)}")
            paper['num_citations'] = 0
    
    # 构建要保存的数据
    date_str = str(datetime.now())
    
    # 创建与原始数据相似的结构
    author_data = {
        'name': 'Yuesheng Huang',
        'citedby': total_citations,
        'updated': date_str,
        'publications': {}
    }
    
    # 添加论文数据
    for paper in papers:
        author_data['publications'][paper['id']] = {
            'num_citations': paper['num_citations'],
            'title': paper['title'],
            'author_pub_id': paper['id']
        }
    
    # 确保目录存在
    print("创建结果目录...")
    try:
        os.makedirs('results', exist_ok=True)
        print(f"结果目录已创建: {os.path.abspath('results')}")
    except Exception as e:
        print(f"创建目录时出错: {str(e)}")
    
    # 保存完整数据
    try:
        print("保存gs_data.json...")
        with open('results/gs_data.json', 'w') as outfile:
            json.dump(author_data, outfile, ensure_ascii=False, indent=2)
        print(f"数据已保存到: {os.path.abspath('results/gs_data.json')}")
    except Exception as e:
        print(f"保存gs_data.json时出错: {str(e)}")
    
    # 保存shields.io格式的数据
    try:
        print("保存gs_data_shieldsio.json...")
        shieldio_data = {
            "schemaVersion": 1,
            "label": "citations",
            "message": f"{total_citations}",
        }
        with open('results/gs_data_shieldsio.json', 'w') as outfile:
            json.dump(shieldio_data, outfile, ensure_ascii=False, indent=2)
        print(f"数据已保存到: {os.path.abspath('results/gs_data_shieldsio.json')}")
    except Exception as e:
        print(f"保存gs_data_shieldsio.json时出错: {str(e)}")
    
    # 列出结果目录内容
    try:
        print("结果目录内容:")
        for file in os.listdir('results'):
            print(f" - {file}")
    except Exception as e:
        print(f"列出目录内容时出错: {str(e)}")
    
    print(f"总引用次数: {total_citations}")
    print(f"数据已保存到 results/gs_data.json 和 results/gs_data_shieldsio.json")
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"执行脚本时出错: {str(e)}")
        sys.exit(1) 
