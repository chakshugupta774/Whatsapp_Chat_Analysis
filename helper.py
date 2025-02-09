from urlextract import URLExtract
from wordcloud import  WordCloud
from collections import Counter
import pandas as pd
import emoji

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
    df = df[df['User'] != 'group notification']
    x = df['User'].value_counts().head()
    # df = round((df['User'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
    #     columns={'index': 'name', 'User': 'percent'})
    df1 = df[df['Message'] == '<Media omitted>\n'].groupby('User').count().sort_values(by="Message", ascending = False).head(10)
    df1 = df1.drop(columns=['Dates','date_only','year','month_name','month','day	hour','minute','day_name','period'],errors='ignore').reset_index()
    return x,df1

def create_wordcloud(selected_user,df):
    if selected_user != 'All':
        df = df[df['User']==selected_user]

    temp = df[df['User']!='group notification']
    temp = temp[temp['Message']!='<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    
    wc = WordCloud(width=500, height=200, min_font_size=10, background_color='white')
    temp['Message'] = temp['Message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['Message'].str.cat(sep=""))
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

def emoji_helper(selected_user, df):
    if selected_user != 'All':
        df = df[df['User']==selected_user]

    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    # emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_counts = Counter(emojis) 
    
    # Create a DataFrame with emoji, count, and description
    emoji_df = pd.DataFrame(
        [(em, count, emoji.demojize(em).replace(":", "").replace("_", " ")) for em, count in emoji_counts.items()],
        columns=['Emoji', 'Count', 'Description']
    )
    emoji_df = emoji_df.sort_values(by="Count", ascending=False).reset_index(drop=True)

    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'All':
        df = df[df['User']==selected_user]
    
    timeline = df.groupby(['year','month','month_name']).count()['Message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month_name'][i]+"-"+str(timeline['year'][i]))
    timeline['time'] = time 
    return timeline 

def daily_timeline(selected_user,df):
    if selected_user != 'All':
        df = df[df['User'] == selected_user]

    daily_timeline = df.groupby('date_only').count()['Message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'All':
        df = df[df['User'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'All':
        df = df[df['User'] == selected_user]
    return df['month_name'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'All':
        df = df[df['User'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='Message', aggfunc='count').fillna(0)

    return user_heatmap

def most_active_days(selected_user,df):
    if selected_user != 'All':
        df = df[df['User'] == selected_user]

    df['Message_count'] = [1] * df.shape[0]       
    active_day_df =df.drop(columns=['year','Dates','User','Message','month_name','month','day','hour','minute','day_name','period'])          
    active_day_df = active_day_df.groupby('date_only').sum().sort_values(by='Message_count',ascending=False).head(10).reset_index()

    return active_day_df