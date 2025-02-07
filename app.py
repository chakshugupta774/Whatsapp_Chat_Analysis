import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import  seaborn as sns

# Title
st.sidebar.title('Whatsapp Chat Analyzer')

# File Uploader
uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None: 
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    #fetch unique users
    user_list = df['User'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,'All')

    selected_user = st.sidebar.selectbox("Show Analysis WRT",user_list)

    if st.sidebar.button('Show Analysis Report'):
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        num_messages, words, links, num_media = helper.fetch_stats(selected_user,df)

        with col1 : 
            st.header('Total Messages')
            st.title(num_messages)
        with col2 : 
            st.header('Total Words')
            st.title(words)
        with col3 : 
            st.header('Media Shared')
            st.title(links)
        with col4 : 
            st.header('Links Shared')
            st.title(num_media)

        
        #Monthly Time analysis  
        st.title('Monthly Time Analysis')
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['Message'])
        plt.xticks(rotation=90)
        st.pyplot(fig)

        #Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['date_only'], daily_timeline['Message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots(figsize=(20,6))
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        #FInding busiest user in the group (group level)
        if selected_user == 'All':
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df,use_container_width=True)

        #WordCloud 
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most Common Words 
        most_common_df = helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation = 'vertical')
        st.title('Most Common Words')
        st.pyplot(fig) 

        #Emoji Analysis 
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df,use_container_width=True)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct='%1.1f%%')
            st.pyplot(fig)
