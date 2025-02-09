import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import  seaborn as sns
import numpy as np

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

    # st.title("Whatsapp Chat Analysis")

    st.markdown(
        "<h1 style='text-align: center;'>Whatsapp Chat Analysis</h1>",
        unsafe_allow_html=True
    )

    if st.sidebar.button('Show Analysis Report'):
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        num_messages, words, links, num_media = helper.fetch_stats(selected_user,df)

        with col1 : 
            st.header('Total Messages')
            st.header(num_messages)
        with col2 : 
            st.header('Total Words')
            st.header(words)
        with col3 : 
            st.header('Media Shared')
            st.header(links)
        with col4 : 
            st.header('Links Shared')
            st.header(num_media)

        
        #Monthly Time analysis  
        st.title('Monthly Time Analysis')
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots(figsize=(13,5))
        ax.plot(timeline['time'],timeline['Message'])
        # plt.xticks(rotation=90)
        plt.xlabel("Month")
        plt.ylabel("Message Count")
        st.pyplot(fig)

        #Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize = (13,5))
        ax.plot(daily_timeline['date_only'], daily_timeline['Message'], color='black')
        # plt.xticks(rotation='vertical')
        plt.xlabel("Date")
        plt.ylabel("Message Count")
        st.pyplot(fig)
        
        #Most Active Days 
        st.title('Most Active Days')
        active_days = helper.most_active_days(selected_user,df)
        fig, ax = plt.subplots(figsize=(13,5))
        x_positions = np.arange(len(active_days['date_only'])) 
        ax.bar(x_positions, active_days['Message_count'], color=plt.cm.viridis(np.linspace(0, 1, len(active_days['date_only']))), width=0.5) 
        ax.set_xticks(x_positions)
        ax.set_xticklabels(active_days['date_only'], ha="center") 
        plt.xlabel("Date")
        plt.ylabel("Message Count")
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.subheader("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            color = sns.color_palette("Spectral", n_colors=10)
            # ax.bar(busy_day.index,busy_day.values,color='purple')
            ax.pie(busy_day,labels=busy_day.index,autopct='%1.1f%%',colors=color)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.subheader("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(5,5))
            colors = sns.color_palette("rocket", n_colors=10)
            ax.barh(busy_month.index, busy_month.values ,color=colors)
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

            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots(figsize=(6,6))
                colors = sns.color_palette("CMRmap", n_colors=10)
                st.subheader('Most Active Users')
                ax.bar(x.index, x.values,color=colors)
                # plt.xticks(rotation='vertical')
                plt.xlabel('User')
                plt.ylabel('Total Message Sent')
                st.pyplot(fig)
            with col2:
                fig, ax = plt.subplots(figsize=(6,6))
                colors = sns.color_palette("CMRmap", n_colors=10)
                # st.dataframe(new_df,use_container_width=True)
                st.subheader('Most Sent Media')
                # ax.pie(new_df['percent'],labels=new_df['name'],autopct='%1.1f%%')
                ax.bar(new_df['User'],new_df['Message'],color=colors)
                plt.xlabel('User')
                plt.ylabel('Total Media Sent')
                st.pyplot(fig)

        #Most Common Words 
        most_common_df = helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots(figsize=(13,5))
        colors = sns.color_palette("viridis", n_colors=10)
        ax.barh(most_common_df[0].head(10),most_common_df[1].head(10),color=colors)
        plt.xticks(rotation = 'vertical')
        st.title('Most Common Words')
        st.pyplot(fig) 

        
        #WordCloud 
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots(figsize=(10,5))
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)

        #Emoji Analysis 
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df.head(10),use_container_width=True)

        with col2:
            fig, ax = plt.subplots(figsize=(5,6))
            colors = sns.color_palette("viridis", n_colors=10)
            ax.barh(emoji_df['Description'].head(10),emoji_df['Count'].head(10),color=colors)
            ax.invert_yaxis()
            st.pyplot(fig)
