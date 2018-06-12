from lxml import html
import requests
import urllib
import urllib.request
import os
import json

NUM_TO_DOWNLOAD = 1000

# URLs of licenses which allow non-commercial redistribution
ALLOW_REDISTRIBUTION = [
    'http://creativecommons.org/licenses/by/4.0/',
    'http://creativecommons.org/licenses/by-sa/4.0/',
    'http://creativecommons.org/licenses/by-nc-sa/4.0/',
    'http://creativecommons.org/publicdomain/zero/1.0/'
]

# URLs of licenses which do not permit redistribution
DISALLOW_REDISTRIBUTION = ['http://arxiv.org/licenses/nonexclusive-distrib/1.0/']

def does_licence_allow_redistribution(url):
    """
    Given a url to an ArXiv abstract, does the article's license permit
    redistribution for non-commericial purposes. Returns true or false if
    license is recognised, and prints error and return false if not.
    """
    license_url = ""
    try:
        page = requests.get(url)
        tree = html.fromstring(page.content)

        abs_div = tree.xpath('//div[@class="abs-license"]')[0]
        abs_a = abs_div.getchildren()[0]
        license_url = abs_a.get('href')

        if license_url in ALLOW_REDISTRIBUTION:
            return True, license_url

        if license_url in DISALLOW_REDISTRIBUTION:
            return False, license_url

        raise BaseException("Did not recognise license at: " + license_url)
    except Exception as e:
        print(e)
        return False, license_url


def scrape_redistributable_pdfs():
    """
    Loop over papers in the Etymo paper metadata JSON file and download the PDFs
    of papers which are redistributable. Starts with the newest entries (end of
    metadata).
    """

    # Open the Etymo metadata json file
    filename = 'OpenData/etymo-10k/papers.json'
    json_data = open(filename).read()
    papers = json.loads(json_data)

    os.makedirs("papers", mode=0o777, exist_ok=True)

    num_downloaded = 0
    i = len(papers) - 1
    while num_downloaded < NUM_TO_DOWNLOAD and i >= 0:
        print("")
        print("Paper: ", i)
        distributable, license_url = does_licence_allow_redistribution(papers[i]["link"])

        if distributable:
            print("Distributable, downloading...", end='', flush=True)
            paper_id = papers[i]["paper_id"]
            paper_folder = "papers/" + str(paper_id) + "/"
            os.makedirs(paper_folder, mode=0o777, exist_ok=True)

            # Download PDF and place in its own folder
            urllib.request.urlretrieve(papers[i]["pdf_link"], paper_folder + "fulltext.pdf")

            # Add a short text file describing the license and source
            with open(paper_folder + 'license.txt', 'w') as f:
                print("License can be found at:", file=f)
                print(license_url, file=f)
                print("", file=f)
                print("Authors can be found at source", file=f)
                print(papers[i]["link"], file=f)

            num_downloaded = num_downloaded + 1
            print(" done. Total downloaded: ", num_downloaded)
        else:
            print("Not distributable, skipping")

        i = i - 1
