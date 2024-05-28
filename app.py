import streamlit as st
import pandas as pd
import numpy as np
import re
import stats
import text_preprocessing
import matplotlib.pyplot as plt

st.sidebar.title('Whatsapp Chat Analyzer')
uploaded_file=st.sidebar.file_uploader('Chose File to upload')

if uploaded_file is not None:
    data=uploaded_file.getvalue()
    data=data.decode("utf-8")
    data=text_preprocessing.preprocess(data)

    user_list=data['users'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user=st.sidebar.selectbox("Show Analysis with respect to",user_list)
    st.title("Whatsapp Chat Analysis for" + selected_user)

    if st.sidebar.button("Show Analysis"):
        num_messages,words,media,num_links=stats.fetchstats(selected_user,data)
        col1, col2, col3, col4 = st.beta_columns(4)

        with col1:
            st.header("Total messages")
            st.title(num_messages)
        
        with col2:
            st.header("Number of words used")
            st.title(words)
        
        with col3:
            st.header("media shared")
            st.title(media)
        
        with col4:
            st.header("Number of links shared")
            st.title(num_links)
        
        if selected_user=='Overall':
            st.title("Most Busy Users")
            busycount,newdata=stats.fetchbusyusers(data)
            fig,ax=plt.subplots()
            col1,col2=st.beta_columns(2)

            with col1:
                ax.bar(busycount.index,busycount.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(newdata)

        st.title("Word cloud")
        data_img=stats.createwordcloud(data,selected_user)
        fig, ax = plt.subplots()
        ax.imshow(data_img)
        st.pyplot(fig)
        

        most_common_words=stats.getcommonwords(selected_user,data)
        fig, ax = plt.subplots()
        ax.barh(most_common_words[0], most_common_words[1])
        plt.xticks(rotation='vertical')
        st.title('Most commmon words')
        st.pyplot(fig)

        emoji_data=stats.getemojistats(selected_user,data)
        emoji_data.columns=['Emoji','Count']
        st.title("Emoji Analysis")
        col1, col2 = st.beta_columns(2)

        with col1:
            st.dataframe(emoji_data)

        with col2:
            emojicount = list(emoji_data['Count'])
            perlist = [(i/sum(emojicount))*100 for i in emojicount]
            emoji_data['Percentage use'] = np.array(perlist)
            st.dataframe(emoji_data)

        st.title("Monthly Timeline")
        time = stats.getmonthtimeline(selected_user, data)
        fig, ax = plt.subplots()
        ax.plot(time['Time'], time['messages'], color='green')
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        st.pyplot(fig)

        st.title("Activity Maps")

        col1, col2 = st.beta_columns(2)

        with col1:

            st.header("Most Busy Day")

            busy_day = stats.weekactivitymap(selected_user, data)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)

        with col2:

            st.header("Most Busy Month")
            busy_month = stats.monthactivitymap(selected_user, data)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)



