#!/usr/bin/env python
# coding: utf-8

# ### Libraries 

# In[1]:


import sys
sys.path.append(r'C:\Users\User\005_Libraries')

import mylibs


# In[2]:


get_ipython().system('pip install anthropic')


# In[3]:


import anthropic
import json
import os
from dotenv import load_dotenv
from glob import glob


# In[11]:


import time
from datetime import datetime


# ### Load the most recent CSV

# In[ ]:





# In[4]:


csv_files= glob('002_Data/gaming_tweets_*.csv')

if csv_files:
    latest_file= sorted(csv_files)[-1]
    
    df_tweets_100= pd.read_csv(latest_file)
    
    print(f"Loaded {len(df_tweets_100)} tweets from: {latest_file}")
    print(f"\nData preview:")
    print(df_tweets_100.head())
    print(f"\nColumns: {list(df_tweets_100.columns)}")
else:
    print("No CSV files found!")


# In[ ]:





# ### Set Up Claude API

# In[ ]:





# In[5]:


load_dotenv()
claude_api_key= os.getenv('ANTHROPIC_API_KEY')

if claude_api_key:
    print("Claude API key found!")
        
    try:
        client= anthropic.Anthropic(api_key= claude_api_key)
        message= client.messages.create(model= "claude-sonnet-4-20250514",
                                        max_tokens= 100,
                                        messages= [{"role": "user", 
                                                    "content": "Say 'Hello, I'm ready to analyze gaming tweets!'"
                                                     }]
                                        )
        
        response= message.content[0].text
        print(f"\nSUCCESS! Claude says: {response}")
                
    except Exception as e:
        print(f"\nConnection error: {e}")
else:
    print("Claude API key still not found!")


# In[ ]:





# ### Analysis Function

# In[6]:


def analyze_tweet(tweet_text):
    """
    Analyze a gaming tweet with Claude AI
    
    Args:
        tweet_text (str): The tweet text to analyze
        
    Returns:
        dict: Analysis with sentiment, topics, entities
    """
    
    prompt= f"""Analyze this gaming tweet and provide structured output in JSON format

Tweet: "{tweet_text}"

Provide analysis in this EXACT JSON format (no additional text):
{{
    "sentiment": "positive/negative/neutral",
    "sentiment_score": 0.0 to 1.0 (0=very negative, 0.5=neutral, 1=very positive),
    "primary_topic": "main topic in 2-3 words",
    "topics": ["topic1", "topic2", "topic3"],
    "entities": {{
        "games": ["game1", "game2"],
        "companies": ["company1"],
        "platforms": ["platform1"],
        "people": ["person1"]
                }},
    "content_type": "complaint/excitement/question/news/review/discussion/other",
    "summary": "one sentence summary"
}}

Return ONLY valid JSON, no markdown, no extra text"""

    try:
        message= client.messages.create(
            model= "claude-sonnet-4-20250514",
            max_tokens= 1000,
            messages= [{"role": "user", 
                        "content": prompt}
                      ])
        
        response_text= message.content[0].text
        
        response_text= response_text.replace('```json', '').replace('```', '').strip()
        
        analysis= json.loads(response_text)
        
        return analysis
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error for tweet: {tweet_text[:50]}...")
        return {
            "sentiment": "neutral",
            "sentiment_score": 0.5,
            "primary_topic": "unknown",
            "topics": [],
            "entities": {"games": [], "companies": [], "platforms": [], "people": []},
            "content_type": "other",
            "summary": "Analysis unavailable"
               }
        
    except Exception as e:
        print(f"API error: {e}")
        return {
            "sentiment": "neutral",
            "sentiment_score": 0.5,
            "primary_topic": "unknown",
            "topics": [],
            "entities": {"games": [], "companies": [], "platforms": [], "people": []},
            "content_type": "other",
            "summary": "Analysis unavailable"
               }

print("✅ Analysis function created!")


# ### Test with ONE Tweet

# In[7]:


test_tweet= df_tweets_100.iloc[0]['text']

print(f"Tweet: {test_tweet[:100]}...")
result= analyze_tweet(test_tweet)

print(json.dumps(result, indent= 2))


# #### Analyze ALL 100 Tweets

# In[12]:


all_results= []

start_time= time.time()

for i, row in df_tweets_100.iterrows():
    tweet_text= row['text']
    
    if (i+1)%10== 0 or i== 0:
        print(f"Processing tweet {i+1}/100...")
    
    analysis= analyze_tweet(tweet_text)
    result= {
        'tweet_id': row['tweet_id'],
        'text': row['text'],
        'created_at': row['created_at'],
        'author_id': row['author_id'],
        'retweet_count': row['retweet_count'],
        'reply_count': row['reply_count'],
        'like_count': row['like_count'],
        'quote_count': row['quote_count'],
        'sentiment': analysis['sentiment'],
        'sentiment_score': analysis['sentiment_score'],
        'primary_topic': analysis['primary_topic'],
        'topics': str(analysis['topics']),
        'games': str(analysis['entities']['games']),
        'companies': str(analysis['entities']['companies']),
        'platforms': str(analysis['entities']['platforms']),
        'people': str(analysis['entities']['people']),
        'content_type': analysis['content_type'],
        'summary': analysis['summary'],
        'analyzed_at': datetime.now()
            }
    
    all_results.append(result)
    
    time.sleep(0.5)

end_time= time.time()
duration= (end_time - start_time)/60

print(f"Analyzed {len(all_results)} tweets!")
print(f"Time taken: {duration:.2f} minutes")
print(f"Estimated cost: ~${len(all_results) * 0.01:.2f}")


# In[13]:


df_analyzed= pd.DataFrame(all_results)

print(f"Rows: {len(df_analyzed)}")
print(f"Columns: {len(df_analyzed.columns)}")
print(df_analyzed.head())


# In[17]:


df_analyzed


# In[ ]:





# ### Save Results to CSV

# In[20]:


timestamp= datetime.now().strftime('%Y%m%d_%H%M%S')
filename= f'002_Data/gaming_tweets_analyzed_{timestamp}.csv'

df_analyzed.to_csv(filename, index= False, encoding= 'utf-8-sig')


# In[ ]:





# ### Alternative way using Src

# In[ ]:


from 001_Src.claude_analyzer import analyze_tweet

all_results= []

start_time= time.time()

for i, row in df_tweets_100.iterrows():
    tweet_text= row['text']
    
    if (i+1)%10== 0 or i== 0:
        print(f"Processing tweet {i+1}/100...")
    
    analysis= analyze_tweet(tweet_text)
    result= {
        'tweet_id': row['tweet_id'],
        'text': row['text'],
        'created_at': row['created_at'],
        'author_id': row['author_id'],
        'retweet_count': row['retweet_count'],
        'reply_count': row['reply_count'],
        'like_count': row['like_count'],
        'quote_count': row['quote_count'],
        'sentiment': analysis['sentiment'],
        'sentiment_score': analysis['sentiment_score'],
        'primary_topic': analysis['primary_topic'],
        'topics': str(analysis['topics']),
        'games': str(analysis['entities']['games']),
        'companies': str(analysis['entities']['companies']),
        'platforms': str(analysis['entities']['platforms']),
        'people': str(analysis['entities']['people']),
        'content_type': analysis['content_type'],
        'summary': analysis['summary'],
        'analyzed_at': datetime.now()
            }
    
    all_results.append(result)
    
    time.sleep(0.5)

end_time= time.time()
duration= (end_time - start_time)/60

print(f"Analyzed {len(all_results)} tweets!")
print(f"Time taken: {duration:.2f} minutes")
print(f"Estimated cost: ~${len(all_results) * 0.01:.2f}")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




