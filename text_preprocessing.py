import streamlit as st
import numpy as np
import pandas as pd
import re
import seaborn as sns

def gettimeanddate(string):
    string=string.split(',')
    date=string[0]
    time=string[1]
    time=time.split('-')
    time=time[0]

    return date + " " + time

def getstring(text):
    return text.split('\n')

def preprocess(data):
    pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\u202f\D{1,2}\s-\s'
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)

    df=pd.DataFrame({'user_messages':messages , 'user_dates':dates})
    df['message_date']=df['message_date'].apply(lambda text:gettimeanddate(text))
    df.rename(columns={'message_date':'date'},inplace=True)

    users=[]
    messages=[]
    for message in df['user_messages']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group Notification')
            messages.append(entry[0])
    
    df['messages']=messages
    df['users']=users

    df['messages']=df['messages'].apply(lambda text:getstring(text)[0])

    df = df.drop(['user_messages'], axis=1)
    df = df[['messages', 'date', 'users']]
    df['Only date'] = pd.to_datetime(df['date']).dt.date

    df['Year'] = pd.to_datetime(df['date']).dt.year

    df['Month_num'] = pd.to_datetime(df['date']).dt.month

    df['Month'] = pd.to_datetime(df['date']).dt.month_name()

    df['Day'] = pd.to_datetime(df['date']).dt.day

    df['Day_name'] = pd.to_datetime(df['date']).dt.day_name()

    df['Hour'] = pd.to_datetime(df['date']).dt.hour

    df['Minute'] = pd.to_datetime(df['date']).dt.minute

    return df

    