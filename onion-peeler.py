import requests
from bs4 import BeautifulSoup
import json
import os

def readSeeds(seedsPath: str):
    seeds = open(seedsPath).readlines()
    return [seed.strip() for seed in seeds if seed.strip() != '']

def getPage(url: str, session):
    page = session.get(url)
    if page is None:
        raise Exception("Page not retrieved")
    return page

def findLinks(page: requests.Response):
    return [str(tag['href']) for tag in BeautifulSoup(page.content, 'html.parser').find_all('a', href=True)]

def clean_links(links):
    return [link for link in links if link.startswith('http')]

def bfsWebCrawling(seedsPath, session):

    with open('tree.json', 'a+') as tree:

        if os.path.isfile('saved_queue.txt'):
            queue = readSeeds('saved_queue.txt')
        else:
            queue = readSeeds(seedsPath)

        count = 0

        tree.write('[')

        while queue:
            try:
                seed = queue.pop(0)

                target = {
                    "parent": seed, 
                    "children": []
                    }
                
                try:
                    page = getPage(seed, session)
                    links = findLinks(page)
                    links = clean_links(links)
                    target['children'] = links

                    print('Writing')                    
                    tree.write(json.dumps(target, indent=4) + ',')
                    print('Done writing')

                    count+=1
                    print('Page' + str(count))

                    queue.extend(links)

                except Exception as e:
                    print(e)
                    continue

            except KeyboardInterrupt:
                tree.write(']')
                savedQueue = open('saved_queue.txt', 'w+')
                savedQueue.write(seed + '\n')
                for link in queue:
                    savedQueue.write(link + '\n')
                savedQueue.close()
                break

            
if __name__ == '__main__':
    session = requests.session()
    session.proxies = {
        'http':  'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    headers = {}
    headers['User-agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0'
    session.headers = headers
    bfsWebCrawling('seeds.txt', session)