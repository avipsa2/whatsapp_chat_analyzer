from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji

extract=URLExtract()
def fetchstats(selected_user,data):
    if selected_user != 'Overall':
        data=data[data['users']==selected_user]
    
    num_messages=data.shape[0]
    words=[]
    for message in data['messages']:
        words.extend(message.split())

    media_omitted=data[data['messages']=='<Media omitted>']
    links=[]
    for message in data['messages']:
        links.extend(extract.find_urls(message))
    
    return num_messages,len(words),media_omitted.shape[0],len(links)

def fetchbusyusers(data):
    data=data[data['users']!='Group Notification']
    count=data['users'].value_counts().head()

    newdata = pd.DataFrame((data['users'].value_counts()/data.shape[0])*100)
    return count,newdata

def createwordcloud(data,selected_user):
    if selected_user != 'Overall':
        data = data[data['users'] == selected_user]
        wc=WordCloud(width=500, height=500,
                   min_font_size=10, background_color='white')
        data_wc=wc.generate(data['messages'].str.cat(sep=" "))

        return data_wc
    
def getcommonwords(selected_user,data):
    file=open('hinglish.txt','r')
    stopwords=file.read()
    stopwords = stopwords.split('\n')

    if selected_user != 'Overall':
        data = data[data['users'] == selected_user]

    temp = data[(data['users'] != 'Group Notification') |
              (data['users'] != '<Media omitted>')]
    words=[]
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    mostcommon=pd.DataFrame(Counter(words).most_common(30))

    return mostcommon

def getemojistats(selected_user,data):
    if selected_user != 'Overall':
        data = data[data['users'] == selected_user]

    emojis=[]
    for i in data['messages']:
        emojis.extend([c for c in i if c in emoji.UNICODE_EMOJI['en']])
    
    emojidata = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emojidata

def getmonthtimeline(selected_user,data):
    if selected_user != 'Overall':
        data = data[data['users'] == selected_user]
    
    temp = data.groupby(['Year', 'Month_num', 'Month']).count()[
        'messages'].reset_index()

    time = []
    for i in range(temp.shape[0]):
        time.append(temp['Month'][i]+"-"+str(temp['Year'][i]))

    temp['Time'] = time

    return temp

def monthactivitymap(selected_user, data):

    if selected_user != 'Overall':
        data = data[data['users'] == selected_user]

    return data['Month'].value_counts()


def weekactivitymap(selected_user, data):

    if selected_user != 'Overall':
        data = data[data['users'] == selected_user]

    return data['Day_name'].value_counts()







