# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 21:32:25 2023

@author: Dell
"""
#Text Preprocessing


"""
extract text from chat and add it to pandas dataframe
"""

import re
import pandas as pd
from datetime import datetime

f= open("WhatsApp Chat group.txt",'r',encoding='utf-8')
data=f.read()
data.replace('\s-\s','\s')
print(data)
#02/04/23, 12:28 am - Abhishek Dutta Kalyani: Jor jor se sabko scheme bata do. sample individual chat structure
pattern =r'\s(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s(?:am|pm))' #first a number with 1 or 2 digits/number with 1 or 2 digits/number with 2 or 4 digits then a comma then space then similar approach for time and then dash- then space

chats = re.split(pattern, data)[1:]
messages = []
for i in range(1,len(chats),2):
    messages.append(chats[i].lstrip(' - '))
print(messages)
dates = re.findall(pattern, data)
times=[]
final_date=[]
#print(dates)# has/u202f encoding, but when evaluating individual records, if you print, you will see it comes as required
for i in range(len(dates)):
    times.append(re.split(", ",dates[i])[1])
    final_date.append(re.split(", ",dates[i])[0])



#Make the dataframe now
df = pd.DataFrame({'user_message':messages,'message_date':final_date,'message_time':times})
afterchangingyear=[]
count=1
for i in df['message_date'].values:
    dd= i.split('/')[0]
    mm= i.split('/')[1]
    yy= i.split('/')[2]
    afterchangingyear.append(dd+'/'+mm+'/'+'20'+yy)
    
    #afterchangingyear.append(i.replace(tochange,'20'+tochange))
#print(afterchangingyear)



df['message_date'] = afterchangingyear
df['combined_time'] = df['message_date']+" "+df['message_time']




#df['message_date'] = pd.to_datetime(df['message_date'])
df['combined_time'] = pd.to_datetime(df['combined_time'])
df.drop(columns=['message_date','message_time'], inplace=True)






#Next task is to separate user's name from the first column. Some lines in the text file are like You have been added. That has to be handled well here.
users=[]
messages=[]
for message in df['user_message']:
    entry = re.split('([\w\W]+?):\s',message)
    #print(entry)
    """
    ['', 'Abhishek Dutta Kalyani', 'https://youtu.be/ZlNFpri-Y40']
    ['', 'Abhishek Dutta Kalyani', 'Supratik left??']
    ['Abhishek Dutta Kalyani added Supratik']
    """
    if(entry[1:]):
        users.append(entry[1])
        messages.append(entry[2])
    else:
        users.append("group notification")
        messages.append(entry[0])
df['user']=users
df['message']=messages
df.drop(columns=['user_message'], inplace=True)

#Now time to extract time,year etc etc
df['year'] = df['combined_time'].dt.year
df['month'] = df['combined_time'].dt.month_name()
df['day'] = df['combined_time'].dt.day
df['hour'] = df['combined_time'].dt.hour
df['minute'] = df['combined_time'].dt.minute
df['second'] = df['combined_time'].dt.second





