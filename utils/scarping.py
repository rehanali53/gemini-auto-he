import requests
from bs4 import BeautifulSoup
tex=[]
websites=["https://www.auto.co.il","https://www.icar.co.il","https://thecar.co.il","https://meshumeshet.com,https://www.cartube.co.il/","https://www.gear.co.il/%D7%9B%D7%AA%D7%91%D7%AA-%D7%A8%D7%9B%D7%91/%D7%9E%D7%92%D7%96%D7%99%D7%9F-%D7%A8%D7%9B%D7%91","https://drivetime.co.il/","https://www.evm.co.il/"]

def scrp():
    try:
        for i,b in enumerate(websites):
            url = b
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()
            data = "\n".join([line for line in text.split('\n') if line.strip() != ''])
            tex.append(data)
    except:
        pass

    return text
