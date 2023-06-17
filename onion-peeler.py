import requests
from bs4 import BeautifulSoup
import json
from progress.bar import Bar

TREE = []

def readSeeds(seedsPath: str):
    seeds = open(seedsPath).readlines()
    return [seed.strip() for seed in seeds]

def getPage(url: str):
    return requests.get(url)

def findLinks(page: requests.Response):
    return [str(tag['href']) for tag in BeautifulSoup(page.content, 'html.parser').find_all('a', href=True)]

def complete_links(links, baseUrl):
    for i in range(len(links)):
        if not links[i].startswith('http'):
            links[i] = baseUrl[:len(baseUrl)-1] + links[i]

def bfsWebCrawling(seedsPath):
    # Create writing file crawler
    tree = open('tree.json', 'a+')
    tree.write('[')
    tree.close()

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
        
        page = getPage(seed)
        links = findLinks(page)
        complete_links(links, seed)
        target['children'] = links
        
        # Improve this shit (I know it sucks)
        tree = open('tree.json', 'a+')
        tree.write(json.dumps(target, indent=4) + ',')
        tree.close()
        
        queue.extend(links)
        bar.next()

    tree = open('tree.json', 'a+')
    tree.write(']')
    tree.close()
    bar.finish()


if __name__ == '__main__':
    bfsWebCrawling('seeds.txt')
