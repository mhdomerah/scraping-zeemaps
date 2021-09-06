## https://www.housinginnovationalliance.com/tools-resources/off-site-heat-map/

import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
        'authority': 'www.zeemaps.com',
        'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^92^\\^, ^\\^',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zeemaps.com/pub?group=3839111&legend=1&search=1&simpleadd=1&track=UA-41067143-4&x=-100.193057&y=43.712520&z=13',
        'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
    }

# Get legends data form zeemap API
def get_legends():
    params = (
        ('g', '3839111'),
    )

    response = requests.get('https://www.zeemaps.com/legends/getall', headers=headers, params=params)
    return response.json()

# Get map point data 
def get_map_data():
    params = (
        ('g', '3839111'),
        ('k', 'REGULAR'),
        ('e', 'true'),
        ('_dc', '0.46430032495452056'),
    )

    response = requests.get('https://www.zeemaps.com/emarkers', headers=headers, params=params)
    return response.json()

# Get eaeh map point detalis
def get_ad_detalis(eid):
    params = (
        ('g', ['3839111', '3839111']),
        ('j', '1'),
        ('sh', ''),
        ('_dc', '0.42354240386822517'),
        ('eids', '^'f'{eid}''^'),
        ('emb', '1'),
    )

    response = requests.get('https://www.zeemaps.com/etext', headers=headers, params=params)
    return response.json()

def main():
    ad_detalis_lst = []
    # Get the id form map data 
    for item in get_map_data():
        _id = item["id"]
        print (_id)

        # Get detalis for each id
        ad_detalis_lst.append(get_ad_detalis(_id))

    # Get detalis from html part 
    ad_html_detalis = []
    for ad in ad_detalis_lst:
        html_dict = {}
        html = ad['t']
        soup = BeautifulSoup(html, "html.parser")

        try:
            html_dict["website"] = soup.find("a")["href"]
        except:
            html_dict["website"] = ""
        
        try:
            html_dict["phone"] = soup.find("span", {"class":"phone"}).text
        except:
            html_dict["phone"] = ""

        for item in soup.find_all("span"):
            html_dict[item.text] = str(item.next_sibling).replace('\xa0','').strip()

        #print (html_dict)
        ad_html_detalis.append(html_dict)

    master_lst  = []

    # Zip tow list to one list 
    for ad,html in zip(ad_detalis_lst,ad_html_detalis):
        final_output = {**ad, **html}
        final_output = {**final_output, **ad["ad"]}
        del final_output["ad"]
        master_lst.append(final_output)

    # Save ziped list to date frame
    df = pd.DataFrame(master_lst)

    # Save data frame to CSV file
    df.to_csv("zeemaps.csv")

# Start script
main()
print ("Done!")
