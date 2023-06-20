import requests
from bs4 import BeautifulSoup
import json
from progress.bar import Bar

def readSeeds(seedsPath: str):
    seeds = open(seedsPath).readlines()
    return [seed.strip() for seed in seeds]

def getPage(url: str, session):
    return session.get(url)

def findLinks(page: requests.Response):
    return [str(tag['href']) for tag in BeautifulSoup(page.content, 'html.parser').find_all('a', href=True)]

def complete_links(links, baseUrl):
    for i in range(len(links)):
        if not links[i].startswith('http'):
            links[i] = baseUrl[:len(baseUrl)-1] + links[i]

def bfsWebCrawling(seedsPath, session):

    with open('tree.json', 'a+') as tree:
    
        tree.write('[')

        # Loads seeds in queue
        queue = readSeeds(seedsPath)

        # Create progress bar
        bar = Bar('Processing', max=200, suffix='%(percent)d%%\n')

        for i in range(250):
            seed = queue.pop(0)

            target = {
                "parent": seed, 
                "children": []
                }
            
            try:
                page = getPage(seed, session)
                links = findLinks(page)
                complete_links(links, seed)
                target['children'] = links
                
                tree.write(json.dumps(target, indent=4) + ',')
                
                queue.extend(links)
            except:
                continue

            bar.next()

        tree.write(']')
        bar.finish()


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
