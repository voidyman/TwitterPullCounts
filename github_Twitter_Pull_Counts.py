#!/usr/bin/env python
# coding: utf-8

# In[4]:


# From here - https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a
# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# For displaying the data after
import pandas as pd
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
import time
from twitter_auth import auth


# In[ ]:


list_of_sites = pd.read_excel("SniffTest_Sources_adfontesmedia.xlsx")


# In[6]:


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


# In[7]:


def create_url(keyword, start_date, end_date, granularity ='hour'):
    
    count_url = "https://api.twitter.com/2/tweets/counts/all" #Change to the endpoint you want to collect data from

    #change params based on the endpoint you are using
    query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'granularity': granularity,
                    'next_token': {}}
    return (count_url, query_params)


# In[8]:


def connect_to_endpoint(url, headers , params=None, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    #print("Endpoint Response Code: " + str(response.status_code))
    
    if response.status_code != 200:
        print("Endpoint Response Code: " + str(response.status_code))
        return 1
    return response.json()


# In[9]:


def get_tweet_counts(url,headers,params,source):
    next_token = None
    flag = True
    small_dfs = []
    retries = 3
    
    while flag:
        print("-------------------")
        print("Token: ", next_token)
        json_response = connect_to_endpoint(url,headers,params,next_token)       
        if (json_response ==1):
            if(retries > 0):
                retries -=1
                print("Check error message - retrying in 60 seconds\n Attempt number:",(5-retries))
                time.sleep(60) 
                continue
            else:
                print("Exceeded 5 retries! Exiting!\nSource :",source, "has incomplete data!")
                break 
        result_count = json_response['meta']['total_tweet_count']
        if 'next_token' in json_response['meta']:
            # Save the token to use for next call
            next_token = json_response['meta']['next_token']
            print("Next Token: ", next_token)    
        else:
            flag=False
        if(result_count>0):
            df = pd.DataFrame.from_dict(json_response['data'])
            df['Source']=source
            print(df.shape[0])
            small_dfs.append(df)
            print("Added:",df["tweet_count"].sum()," from ",source)
        
        print("total tweets :",result_count)
        print("-------------------")
        time.sleep(5) 
    
    if(small_dfs):
        result = pd.concat(small_dfs, ignore_index=True)
        return result


# In[10]:


bearer_token = auth()
headers = create_headers(bearer_token)
start_time = "2021-09-01T11:40:00.00z"
end_time = "2021-11-10T11:40:00.00z"
granularity = 'hour'


# In[11]:


for idx,row in list_of_sites.iterrows():
    
    if(row["Type"]=="Website"):
        source = row["URL_stub"]+".com"
        keyword = '(url:\"'+source+'\") -is:retweet -(FB OR Facebook OR WhatsApp OR Insta OR Instagram)'
        [url,params] = create_url(keyword,start_time,end_time,granularity)
        results = get_tweet_counts(url,headers,params,source)
        if (results is None):
            print("NO RESULTS FOR ",source)
            continue
        else:
            results.to_csv("TweetCounts_"+row["URL_stub"]+".csv",index=False)
    else:
        print(row["URL_stub"], "Is not a website. Ignoring\n")

print("DONE")


# In[ ]:




