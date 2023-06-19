import requests
from bs4 import BeautifulSoup
import json
from progress.bar import Bar
from torrequest import TorRequest

def readSeeds(seedsPath: str):
    seeds = open(seedsPath).readlines()
    return [seed.strip() for seed in seeds]

def getPage(url: str, session):
    return session.get(url)

def getTorPage(url: str):
    with TorRequest() as tr:
        print(tr.get(url).text)

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
            
            page = getPage(seed, session)
            links = findLinks(page)
            complete_links(links, seed)
            target['children'] = links
            
            tree.write(json.dumps(target, indent=4) + ',')
            
            queue.extend(links)
            bar.next()

        tree.write(']')
        bar.finish()


if __name__ == '__main__':
    getTorPage('http://http://tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion/')
