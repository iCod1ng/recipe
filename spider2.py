import requests
import json
import re
from requests.exceptions import RequestException
from multiprocessing import Pool
def parse_one_page(html):
    pattern = re.compile('<div.*?info pure-u.*?name">(.*?)<.*?ellipsis">(.*?)</p>'
                         +'.*?green-font">(.*?)</span>.*?</div>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'name':item[0].strip(),
            'elem':item[1].strip(),
            'score':item[2].strip()
        }
def write_to_file(content):
    with open('recipe.txt','a',encoding='utf-16') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
def main(page):
    url = 'http://www.xiachufang.com/category/40076/?page='+str(page)
    html = get_one_page(url)
    for item in parse_one_page(html):
       print(item)
       write_to_file(item)
if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i for i in range(1,11)])