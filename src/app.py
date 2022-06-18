# your app code here
#pip install pandas sqlite3 requests
import pandas as pd
import requests
import sqlite3
from bs4 import BeautifulSoup

#read from source
url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text

#parse the html data, html code
soup = BeautifulSoup(html_data,"html.parser")

#search the table tag
tablas=soup.findAll("table")

#search the table index of "Tesla Quarterly Revenue"
index_find=0
for i, tabla in(enumerate(tablas)):
    #enumarate asigna i=indice tabla=contenido
    if ("Tesla Quarterly Revenue" in str(tabla)):
        index_find=i

#print(tablas[index_find])


#go inside table and save the values
#df=pd.DataFrame(columns=["date","revenue"])

dataValues = []
#df = pd.DataFrame()
for rowT in tablas[index_find].tbody.find_all("tr"):
    #for each tr (row), take the td (column) value
    colT= rowT.find_all("td")
    if len(colT)>0:
        dateVal=colT[0].text
    revenueVal=colT[1].text.replace("$","").replace(",","")
    #print(dateVal," ",revenueVal)
    dataValues.append({"date":dateVal,"revenue":revenueVal})

#df = df.append({"date":dateVal,"revenue":revenueVal},ignore_index=True)
#deprecated method.

#load data to the dataframe
df = pd.DataFrame.from_records(dataValues)
#print(df.tail(10))

#not null in exploration, if find use dropna
#quito vacios
df=df[df["revenue"] != ""]

#change type
df['date'] = df['date'].astype('datetime64')
df['revenue'] = df['revenue'].astype('int64')

###### STEP DATABASE #########

#create the file where save the database if not exists yet
conn = sqlite3.connect('Tesla.db') 
c = conn.cursor()

#load the dataframe to the database
df.to_sql("Tesla",conn,if_exists='replace',index=False)

conn.commit()

#read from database the data
sel_df = pd.read_sql("select * from Tesla",conn)
print(sel_df)

conn.close()


df.plot(kind="scatter",x="date",y="revenue")

import matplotlib.pyplot as plt
df.hist(bins=50, figsize=(15,15))
plt.show()

