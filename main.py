import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
PATH = "C:\Program Files (x86)\msedgedriver.exe"
driver = webdriver.Edge(PATH)
driver.get('http://museus.cultura.gov.br/busca/##(global:(enabled:(space:!t),filterEntity:space,viewMode:list),space:(filters:(En_Estado:!(AL))))')
table = {'Museus':[], 'Sites':[]}
SCROLL_PAUSE_TIME = 0.5

last_height = driver.execute_script("return document.body.scrollHeight")

for i in range(0,10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

links = driver.find_elements_by_tag_name('h1')
for elements in links:
    try:
        x = elements.find_element_by_tag_name('a')
        if x.text != '' and x.text != "Museus":
            req = requests.get(x.get_attribute('href'))
            if req.status_code == 200:
                print('Requisição bem sucedida!')
                content = req.content
            soup = BeautifulSoup(content, 'html.parser')
            try:
                link = soup.find(name='a', attrs={'class': 'url'})['href']
                table['Museus'].append(x.text)
                table['Sites'].append(link)
            except:
                pass
    except:
        pass
driver.quit()
df = pd.DataFrame(data= table)
print(df)
df.to_csv('Museus.csv')