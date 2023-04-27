import os
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# 下载cif文件的保存目录
save_dir = 'D:/code/cod/2elements'

# cif文件URL列表的文本文件
url_file = os.path.join(save_dir, 'COD-selection.txt')

# 已下载cif文件的列表
downloaded_files = os.listdir(save_dir)

# 读取cif文件的URL列表，并跳过已下载的文件
with open(url_file, 'r') as f:
    cif_urls = f.readlines()
    cif_urls = [url.strip() for url in cif_urls
                if url.split('/')[-1] not in downloaded_files]

# 下载单个cif文件的函数
def download_cif(cif_url):
    cif_url = cif_url.strip()  # 去除URL字符串中的空格、换行符等
    cif_id = cif_url.split('/')[-1].split('.')[0]  # 从URL中提取cif文件编号
    cif_file = os.path.join(save_dir, cif_id+'.cif')
    response = requests.get(cif_url, stream=True)
    with open(cif_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

# 使用多线程下载cif文件
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = []
    for cif_url in cif_urls:
        futures.append(executor.submit(download_cif, cif_url))
    for f in tqdm(futures):
        f.result()