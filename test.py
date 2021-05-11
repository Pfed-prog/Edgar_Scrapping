from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


soup = []
source = ''

for x in range(20):
    time.sleep(1) 
    source = requests.get(f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&SIC=2834&owner=include&match=&start={x}00&count=100&hidefilings=0').content

    if not BeautifulSoup(source, 'lxml').find_all('td'):
        #print('rerun')
        time.sleep(2)
        source = requests.get(f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&SIC=2834&owner=include&match=&start={x}00&count=100&hidefilings=0').content
        if not BeautifulSoup(source, 'lxml').find_all('td'):
            time.sleep(2)
            source = requests.get(f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&SIC=2834&owner=include&match=&start={x}00&count=100&hidefilings=0').content
            if not BeautifulSoup(source, 'lxml').find_all('td'):
                break

    #print(BeautifulSoup(source, 'lxml').find_all('td')[:1])
    soup.append(BeautifulSoup(source, 'lxml').find_all('td'))


# 10 integers
# name
# state

comp_name, comp_state, comp_num = [], [], []

for page in soup:
    i=3
    for line in page:
        if i % 3 == 0:
            comp_num.append(line.text)
        if i % 3 == 1:
            comp_name.append(line.text)
        if i % 3 == 2:
            comp_state.append(line.text)
        i+=1


df = pd.DataFrame({'company': comp_name, 'number':comp_num, 'state': comp_state})
df.to_csv('project.csv')
print(df.tail())
#https://pypi.org/project/edgar/