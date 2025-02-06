import re 
import pandas as pd

def preprocess(data):
    pattern = '\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\s?[ap]m -'

    #Splitting the data into User_Messages and Dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    dates = [date.replace("\u202f", " ") for date in dates]

    #Create DataFrame of User_Messages and Dates 
    df = pd.DataFrame({'User_message':messages, 'Dates':dates})

    #Cleaning the Dates
    df['Dates'] = pd.to_datetime(df['Dates'],format="%d/%m/%y, %I:%M %p -")

    #Cleaning the User_Messages
    user = []
    message = []
    for messages in df['User_message']:
        entry = re.split('([\w\W]+?):\s',messages)
        if entry[1:]: #user entry 
            user.append(entry[1])
            message.append(" ".join(entry[2:]))
        else:
            user.append('group notification')
            message.append(entry[0])

    df['User'] = user
    df['Message'] = message
    df.drop(columns=['User_message'],inplace=True)

    #Extracting Date, Year, Month, Day, Hour, Minute, Day_name
    df['date_only'] = df['Dates'].dt.date
    df['year'] = df['Dates'].dt.year
    df['month_name'] = df['Dates'].dt.month_name()
    df['month'] = df['Dates'].dt.month
    df['day'] = df['Dates'].dt.day
    df['hour'] = df['Dates'].dt.hour
    df['minute'] = df['Dates'].dt.minute
    df['day_name']= df['Dates'].dt.day_name()

    return df