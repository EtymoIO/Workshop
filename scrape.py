from lxml import html
import requests
import urllib
import urllib.request
import os

NUM_TO_DOWNLOAD = 1000

ALLOW_REDISTRIBUTION = [
    'http://creativecommons.org/licenses/by/4.0/',
    'http://creativecommons.org/licenses/by-sa/4.0/',
    'http://creativecommons.org/licenses/by-nc-sa/4.0/',
    'http://creativecommons.org/publicdomain/zero/1.0/'
]

DISALLOW_REDISTRIBUTION = ['http://arxiv.org/licenses/nonexclusive-distrib/1.0/']

def does_licence_allow_redistribution(url):

    print(url)
    page = requests.get(url)
    tree = html.fromstring(page.content)

    abs_div = tree.xpath('//div[@class="abs-license"]')[0]
    abs_a = abs_div.getchildren()[0]
    license_url = abs_a.get('href')

    if license_url in ALLOW_REDISTRIBUTION:
        return True, license_url

    if license_url in DISALLOW_REDISTRIBUTION:
        return False, license_url

    print(license_url)
    raise BaseException("Could not find licence")

import json

def scrape_redistributable_pdfs():
    filename = 'OpenData/etymo-10k/papers.json'
    json_data = open(filename).read()
    papers = json.loads(json_data)

    # os.makedirs("papers", mode=0o777, exist_ok=True)

    num_downloaded = 0
    i = 7
    while num_downloaded < NUM_TO_DOWNLOAD:
        print("Paper: ", i)
        # print(papers[i])
        distributable, license_url = does_licence_allow_redistribution(papers[i]["link"])

        print("Distributable", distributable)
        if distributable:
            paper_id = papers[i]["paper_id"]
            paper_folder = "papers/" + str(paper_id) + "/"
            os.makedirs(paper_folder, mode=0o777, exist_ok=True)
            # urllib.request.urlretrieve(papers[i]["pdf_link"], paper_folder + str(paper_id) + ".pdf")
            with open(paper_folder + 'licence.txt', 'w') as f:
                print("Licence can be found at:", file=f)
                print(license_url, file=f)
                print("", file=f)
                print("Authors can be found at source", file=f)
                print(papers[i]["link"], file=f)

            num_downloaded = num_downloaded + 1

        i = i + 1
