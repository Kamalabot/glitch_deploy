"""Program to analyse the given youtube Channel or Playlist"""
from typing import List
#importing pytube modules
from pytube import YouTube
from pytube import Channel
from pytube import Search
#import scrapetube to get the videos from the channel
import scrapetube as sct
#importing pandas for dataframe support
import pandas as pd
import os
#import streamlit
import streamlit as st

st.write("""
         ## Find the best videos of the Youtube Channel or Playlist
         """)
#getting user input
your_link = st.text_input("Paste any youtube video link")


#list to store the youtube links
youtube_links = []


def get_video_links(your_link:str):
    """Function that returns the list of links 
    the channel has from the given youtube video"""
    vidObj = YouTube(your_link)
    
    #get channel url
    channelURL = vidObj.channel_url
    
    #get channel obj
    channelObj = Channel(channelURL)
    
    #get channel name
    channel_name = channelObj.channel_name 
    
    #writing out the channel name
    st.write(f'The Channel name is {channel_name}')
    
    #get Channel ID
    channel_ref_id = channelObj.channel_id
    
    #get the video list
    video_gen = sct.get_channel(channel_ref_id)

    for vids in video_gen:
        youtube_links.append(f"https://www.youtube.com/watch?v={vids['videoId']}")

    return youtube_links

def get_vid_views(link):
    vid_t = YouTube(link)
    try:
        return vid_t.views
    except TypeError as e:
        return 0

def get_top_videos(links:List[str], no_vids:int):
    top_vids = []
    
    for l in links:
        #print(l)
        view = get_vid_views(l)
        top_vids.append([l, view])
    #print(top_vids)
    return_vids = sorted(top_vids,key=lambda x: x[1],reverse=True)
    return return_vids[:no_vids]

def get_vid_data(link):
    """Gets all important information about the given link"""
    vid_t = YouTube(link)
    keys = ','.join(vid_t.keywords)
    cha = Channel(vid_t.channel_url)
    data = {'Author':vid_t.author,'title':vid_t.title, 'Age_restriction':vid_t.age_restricted,'description':vid_t.description,
                'keywords':keys, 'length':vid_t.length,'publish_date':vid_t.publish_date,'views':vid_t.views,
                'about':cha.about_url, 'vid_link':link}
    vid_df = pd.DataFrame(data,index=[0])
    return vid_df

def dataframe_collector(linklist):
    """Returns the dataframe with the details of the videos in the channel"""
    vid_collector = pd.DataFrame()
    x = len(linklist)
    for link in linklist:
        c_data = get_vid_data(link)
        vid_collector = pd.concat([vid_collector,c_data])
        if vid_collector.shape[0]//10 == 0:
            print('Completing {} % of list'.format((vid_collector.shape[0]/x)*100))
    return vid_collector

#Initiate video object 
if your_link:
    st.write(your_link)
    #get all the links in the channel
    st.write("## Hold on... fetching you the top videos in this channel")
    all_links = get_video_links(your_link)
    st.write("""## Okay, I have fetched them. Here are the ten links""") 
    st.write(all_links[:10])
    #find the links with top views
    vids_with_top_view = get_top_videos(all_links, 20)
    #Write the links out
    #st.write("##Top 20 Videos in this channel:")
    st.write("""Let me fetch you the videos with top views""")
    top_vid_links = [link[0] for link in vids_with_top_view]
    #st.write(top_vid_links)
    vid_df = pd.DataFrame(vids_with_top_view,columns=['videos','views'])
    st.bar_chart(vid_df,x='videos',y='views')
    st.table(vid_df)
    
    
#want_data = st.text_input("Enter 'Yes' if you want more details on the above videos")
    #get the details of top videos as dataframe
#if want_data == 'Yes':
#    vids_dataframe = dataframe_collector(top_vid_links) 
#    st.write("## Videos details:")
#    st.write(vids_dataframe)
#else:
#    st.write("Thanks for Viewing the page!!!")

