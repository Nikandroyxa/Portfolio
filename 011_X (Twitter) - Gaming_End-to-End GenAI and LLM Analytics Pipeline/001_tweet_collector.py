#!/usr/bin/env python
# coding: utf-8

# ### Libraries

# In[1]:


import sys
sys.path.append(r'C:\Users\User\005_Libraries')
import mylibs


# In[2]:


get_ipython().system('pip install tweepy')


# In[3]:


import tweepy
from dotenv import load_dotenv
import os
from datetime import datetime


# In[ ]:





# ### Store Bearer Token in a .env file (secure)

# #### Create .gitignore (GitHub protection)

# In[4]:


git_ignore= """
    .env
    *.env
    __pycache__/
    *.pyc
    .ipynb_checkpoints/
    .DS_Store
    Thumbs.db
"""

with open('.gitignore', 'w') as f:
    f.write(git_ignore)


# In[5]:


api_key= input('Paste your API Key: ').strip()
api_secret= input('Paste your API Key Secret: ').strip()
bearer_token= input('Paste your Bearer Token: ').strip()
claude_key= input("Claude API Key: ").strip()

env_file= f"""# ============================================
# TWITTER/X API CREDENTIALS
# ============================================

# Consumer Keys
TWITTER_API_KEY={api_key}
TWITTER_API_KEY_SECRET={api_secret}

# Authentication Token
BEARER_TOKEN={bearer_token}

# ============================================
# CLAUDE API CREDENTIALS
# ============================================

ANTHROPIC_API_KEY={claude_key}
"""

with open('.env', 'w') as f:
    f.write(env_file)
    
from IPython.display import clear_output
import time

time.sleep(5)
clear_output()


# #### Check the .env file

# In[6]:


try:
    with open('.env', 'r') as f:
        content= f.read()
        print(content)
except FileNotFoundError:
    print(".env file not found!")
    

time.sleep(5)
clear_output()


# In[7]:


with open('.env', 'r') as f:
    print(f.read())

time.sleep(5)
clear_output()


# In[8]:


get_ipython().system('type .env')

time.sleep(5)
clear_output()


# In[ ]:





# ### Test Twitter connection

# In[ ]:





# In[9]:


load_dotenv()
bearer_token= os.getenv('BEARER_TOKEN')

try:
    client= tweepy.Client(bearer_token= bearer_token)
    
    response= client.search_recent_tweets(query= "gaming", max_results= 10)
    
    print("\nSUCCESS! Connected to Twitter API!")
    print(f"Found {len(response.data)} tweets about gaming!")
    print("\nFirst tweet preview:")
    print(f"{response.data[0].text[:100]}...")
    
except Exception as e:
    print(f"ERROR: {e}")


# In[ ]:





# ### Collect 100 Gaming Tweets

# In[ ]:





# In[ ]:


response= client.search_recent_tweets(
                                      query= "gaming -is:retweet lang:en",
                                      max_results =100,
                                      tweet_fields= ['created_at', 'public_metrics', 'lang', 'author_id']
                                      )

print(f"Collected {len(response.data)} tweets!")
print(f"First tweet: {response.data[0].text[:80]}...")


# In[ ]:





# ### Extract Data into a Nice Table

# In[ ]:





# In[ ]:


tweets_data= []

for tweet in response.data:
    tweet_info= {
                 'tweet_id': tweet.id,
                 'text': tweet.text,
                 'created_at': tweet.created_at,
                 'author_id': tweet.author_id,
                 'lang': tweet.lang,
                 'retweet_count': tweet.public_metrics['retweet_count'],
                 'reply_count': tweet.public_metrics['reply_count'],
                 'like_count': tweet.public_metrics['like_count'],
                 'quote_count': tweet.public_metrics['quote_count'],
                 'collected_at': datetime.now()
                }
    tweets_data.append(tweet_info)

df= pd.DataFrame(tweets_data)
print(df.head())
print(f"\nTotal tweets: {len(df)}")


# In[ ]:





# ### Save to CSV File

# In[ ]:





# In[ ]:


os.makedirs('002_Data', exist_ok= True)
timestamp= datetime.now().strftime('%Y%m%d_%H%M%S')
filename= f'002_Data/gaming_tweets_{timestamp}.csv'

df.to_csv(filename, index= False, encoding= 'utf-8-sig')


# In[ ]:





# In[10]:


csv_path= '002_Data/gaming_tweets_20251218_142234-Copy1.csv'

if os.path.exists(csv_path):
    df= pd.read_csv(csv_path)


# In[13]:


df.info()


# In[ ]:




