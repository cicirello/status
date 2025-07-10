from urllib.request import urlopen, Request
from urllib.error import HTTPError
from lxml import html
import json

user_agent = 'Mozilla/5.0'
url = 'https://github.com/cicirello/jacoco-badge-generator/network/dependents?package_id=UGFja2FnZS0yOTQ0NTMxNTI3'
output_file = 'jacoco-badge-generator.json'

def get():
    try :
        with urlopen(Request(url, headers={'User-Agent' : user_agent})) as response :
            return response.read().decode(response.headers.get_content_charset())
    except HTTPError as e:
        print("ERROR: Failed to retrieve the dependents page!")
        print(e.status)
        print(e.reason)
        print(e.headers)
        print("Exiting....")
        exit(1)

def extract(page):
    tree = html.fromstring(page)
    count = tree.xpath('//*[@id="dependents"]/div[2]/div[1]/div/div[1]/a[1]/text()')
    count = " ".join(count)
    count = count[:count.find('Repositories')].strip()
    return count

def output(count):
    try:
        with open(output_file, "w") as jsonFile :
            json.dump(count, jsonFile, indent=4, sort_keys=True)
    except IOError:
        print("Error: An error occurred while writing the json file.")
        exit(1)

if __name__ == '__main__':
    output({
        "message" : extract(get()),
        "schemaVersion" : 1,
        "label" : "used by",
        "color" : "blue",
        "namedLogo" : "GitHub"
    })
