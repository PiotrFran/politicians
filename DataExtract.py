from selenium import webdriver
import bs4 as bs
import pandas as pd
import urllib.request

print(soup.title.parent.name)

politicians=pd.DataFrame(columns=['Politician','Redirect'])

def politician_list():
    global politicians
    base='https://www.sejm.gov.pl/Sejm9.nsf/wypowiedzi.xsp'
    source = urllib.request.urlopen('https://www.sejm.gov.pl/Sejm9.nsf/wypowiedzi.xsp?view=5').read()
    soup = bs.BeautifulSoup(source,'lxml')
    uls = soup.find_all('ul', {'class': 'category-list'})
    for ul in uls:
        for li in ul.find_all('li'):
            for link in li.find_all('a'):
                url = link.get('href')
                contents = link.text
                if url != None:
                    politicians=politicians.append({'Politician' : contents , 'Redirect' : base+url} , ignore_index=True)
                #print (url, contents)

politician_list()
politicians

# politician_statements=pd.DataFrame(columns=['Politician','Title','Statement','Redirect',])
# statements1=politicians.iloc[10,1]
# politician1=politicians.iloc[10,0]


# base2='https://www.sejm.gov.pl/Sejm9.nsf/'
# source = urllib.request.urlopen(statements1).read()
# soup2=bs.BeautifulSoup(source,'lxml')
# table = soup2.find('table', 'table border-bottom lista-wyp')
# for link in table.findAll('a', class_=[]):
# url = link.get('href')
# contents = link.text
# politician_statements=politician_statements.append({'Politician' : politician1 ,'Title': contents,  'Redirect' : base2+url} , ignore_index=True)
# print (url, contents)

politician_statements=pd.DataFrame(columns=['Politician','Statement','Redirect'])
def statement_list(politician,link):
    global politician_statements
    base2='https://www.sejm.gov.pl/Sejm9.nsf/'
    source = urllib.request.urlopen(link).read()
    soup2=bs.BeautifulSoup(source,'lxml')
    table = soup2.find('table', 'table border-bottom lista-wyp')
    for link in table.findAll('a', class_=[]):
        url = link.get('href')
        contents = link.text
        politician_statements=politician_statements.append({'Politician' : politician,  'Redirect' : base2+url} , ignore_index=True)
        print(politician_statements)

def statements_redirects():
    global politician_statements
    politician_statements=pd.DataFrame(columns=['Politician','Statement','Redirect'])
    for index, row in politicians.iterrows():
        statement_list(row['Politician'],row['Redirect'])

statements_redirects()
politician_statements.groupby('Politician').count()
politician_statements