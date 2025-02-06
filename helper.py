from urlextract import URLExtract
from wordcloud import  WordCloud
from collections import Counter
import pandas as pd

f = open('stop_hinglish.txt')
stop_words = f.read()
extractor = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'All':
        df = df[df['User']==selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['Message']:
        words.extend(message.split())

    links = []
    for message in df['Message']:
        links.extend(extractor.find_urls(message)) 

    num_media = df[df['Message']=='<Media omitted>\n'].shape[0]

    return num_messages, len(words), len(links), num_media


def most_busy_user(df):
    x = df['User'].value_counts().head()
    df = round((df['User'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'User': 'percent'})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != 'All':
        df = df[df['User']==selected_user]
    
    wc = WordCloud(width=500, height=200, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['Message'].str.cat(sep=""))
    return df_wc

def most_common_words(selected_user, df):
    if selected_user != 'All':
        df = df[df['User']==selected_user]

    temp = df[df['User']!='group notification']
    temp = temp[temp['Message']!='<Media omitted>\n']

    words = []
    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df