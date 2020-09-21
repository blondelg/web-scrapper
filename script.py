import pandas as pd
from bs4 import BeautifulSoup
import requests
import json



def get_ad_urls(url):
    """ From a ad listing view, return a list of ad urls """
    result = []
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    for e in soup.find_all("div", {"class": "adContainer"}):
        sub_soup = BeautifulSoup(e.decode_contents(), "html.parser")
        result.append(sub_soup.find("a")['href'])
    return result
    

def get_lising_next(url):
    """ From a listing view, return the next listing page url """
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    for e in soup.find_all("li", {"class": "arrow-btn"}):
        if "suivante" in e.decode_contents():
            return e.find("a")['href']
            
            
def get_data(url):
    """ From a ad page, return desired data """
    try:
        url_template = 'https://www.lacentrale.fr{}'
        html = requests.get(url_template.format(url))
        soup = BeautifulSoup(html.text, "html.parser")
        soup.find("div", {"id": "trackingStateContainer"}).getText()
        json_data = json.loads(soup.find("div", {"id": "trackingStateContainer"}).getText())

        return {'prix': json_data['vehicle']['price']['price'],
                'marque': json_data['vehicle']['make'],
                'model': json_data['vehicle']['model'],
                'energie': json_data['vehicle']['energy'],
                'année': json_data['vehicle']['year'],
                'codepostal': json_data['vehicle']['zipcode'],
                'puissance': json_data['vehicle']['powerDIN'],
                'km': json_data['vehicle']['mileage']}
    
    except Exception as e:
        print("Error : {}".format(e))
        return None
        
        
# Script
if __name__ == '__main__':
    url = '/listing?energies=ess&gearbox=AUTO&makesModelsCommercialNames=PEUGEOT&regions=FR-BRE'
    url_template = 'https://www.lacentrale.fr{}'
    ad_list = []

    # Get url list of ads
    while url:
        ad_list += get_ad_urls(url_template.format(url))
        url = get_lising_next(url_template.format(url))
        
    # Store data in a DataFrame
    df = pd.DataFrame()

    # Append DataFrame
    for ad_url in ad_list:
        data = get_data(ad_url)
        if data:
            df = df.append(data, ignore_index=True)
            
    print(df)

