#!/usr/bin/env python
# coding: utf-8

# ### Libraries 

# In[1]:


import sys
sys.path.append(r'C:\Users\User\005_Libraries')

import mylibs


# In[10]:


from collections import Counter
from datetime import datetime


# ### Sentiment Analysis

# In[2]:


df_analyzed= pd.read_csv('002_Data/gaming_tweets_analyzed_20260110_122738.csv')
df_analyzed


# In[3]:


sentiment_counts= df_analyzed['sentiment'].value_counts()

for sentiment, count in sentiment_counts.items():
    percentage= (count / len(df_analyzed)) * 100
    print(f"{sentiment.capitalize():10s}: {count:3d} tweets ({percentage:5.1f}%)")


# In[4]:


avg_sentiment= df_analyzed['sentiment_score'].mean()

print(f"\nAverage Sentiment Score: {avg_sentiment:.2f}")


# In[5]:


most_positive= df_analyzed.loc[df_analyzed['sentiment_score'].idxmax()]

print(f"Score: {most_positive['sentiment_score']:.2f}")
print(f"Text: {most_positive['text'][:100]}...")


# In[6]:


most_negative= df_analyzed.loc[df_analyzed['sentiment_score'].idxmin()]

print(f"Score: {most_negative['sentiment_score']:.2f}")
print(f"Text: {most_negative['text'][:100]}...")


# ### Topics Analysis

# In[7]:


top_topics= df_analyzed['primary_topic'].value_counts().head(10)

for i, (topic, count) in enumerate(top_topics.items(), 1):
    print(f"{i:2d}. {topic:30s} ({count:2d} tweets)")


# In[8]:


content_types= df_analyzed['content_type'].value_counts()

for content_type, count in content_types.items():
    percentage= (count / len(df_analyzed)) * 100
    print(f"{content_type.capitalize():12s}: {count:3d} tweets ({percentage:5.1f}%)")


# ### Entities Analysis (Games, Companies, Platforms)

# In[11]:


all_games= []

for games_str in df_analyzed['games']:
    try:
        games= eval(games_str)
        all_games.extend(games)
    except:
        pass

if all_games:
    game_counts= Counter(all_games)
    print(f"\nMost Mentioned Games (found {len(game_counts)} unique games):")
    for i, (game, count) in enumerate(game_counts.most_common(10), 1):
        print(f"{i:2d}. {game:30s} ({count:2d} mentions)")
else:
    print("\nMost Mentioned Games: No games detected")


# In[12]:


all_companies= []
for companies_str in df_analyzed['companies']:
    try:
        companies= eval(companies_str)
        all_companies.extend(companies)
    except:
        pass

if all_companies:
    company_counts= Counter(all_companies)
    print(f"\nMost Mentioned Companies (found {len(company_counts)} unique companies):")
    for i, (company, count) in enumerate(company_counts.most_common(10), 1):
        print(f"   {i:2d}. {company:30s} ({count:2d} mentions)")
else:
    print("\nMost Mentioned Companies: No companies detected")


# In[13]:


all_platforms= []
for platforms_str in df_analyzed['platforms']:
    try:
        platforms= eval(platforms_str)
        all_platforms.extend(platforms)
    except:
        pass

if all_platforms:
    platform_counts= Counter(all_platforms)
    print(f"\nMost Mentioned Platforms (found {len(platform_counts)} unique platforms):")
    for i, (platform, count) in enumerate(platform_counts.most_common(10), 1):
        print(f"   {i:2d}. {platform:30s} ({count:2d} mentions)")
else:
    print("\nMost Mentioned Platforms: No platforms detected")


# ### Summary Statistics

# In[14]:


print("\nTweet Engagement:")
print(f"Total Retweets:  {df_analyzed['retweet_count'].sum():,}")
print(f"Total Replies:   {df_analyzed['reply_count'].sum():,}")
print(f"Total Likes:     {df_analyzed['like_count'].sum():,}")
print(f"Total Quotes:    {df_analyzed['quote_count'].sum():,}")

print("\nAverage Engagement per Tweet:")
print(f"Avg Retweets:    {df_analyzed['retweet_count'].mean():.2f}")
print(f"Avg Replies:     {df_analyzed['reply_count'].mean():.2f}")
print(f"Avg Likes:       {df_analyzed['like_count'].mean():.2f}")
print(f"Avg Quotes:      {df_analyzed['quote_count'].mean():.2f}")

print("\nSentiment vs Engagement:")
for sentiment in df_analyzed['sentiment'].unique():
    sentiment_tweets= df_analyzed[df_analyzed['sentiment']== sentiment]
    avg_likes= sentiment_tweets['like_count'].mean()
    print(f"{sentiment.capitalize():10s} tweets: {avg_likes:.2f} avg likes")


# In[ ]:





# ### Visualization Dashboard

# In[28]:


# Visualization dashboard
fig, axes= plt.subplots(2, 3, figsize= (18, 12))
fig.suptitle('Gaming Tweets AI Analysis Dashboard', fontsize= 20, fontweight= 'bold', y= 0.995)

# === 1. Sentiment Distribution (Pie Chart) ===
sentiment_counts= df_analyzed['sentiment'].value_counts()
colors= ['#2ecc71', '#95a5a6', '#e74c3c']
axes[0, 0].pie(sentiment_counts, labels= sentiment_counts.index, autopct= '%1.1f%%', 
               startangle= 90, colors= colors, textprops= {'fontsize': 11})
axes[0, 0].set_title('Sentiment Distribution', fontsize= 14, fontweight= 'bold', pad= 10)

# === 2. Sentiment Scores (Histogram) ===
axes[0, 1].hist(df_analyzed['sentiment_score'], bins= 20, color= '#3498db', edgecolor= 'black', alpha= 0.7)
axes[0, 1].axvline(df_analyzed['sentiment_score'].mean(), color= 'red', linestyle= '--', 
                   linewidth= 2, label= f'Mean: {df_analyzed["sentiment_score"].mean():.2f}')
axes[0, 1].set_xlabel('Sentiment Score', fontsize= 11)
axes[0, 1].set_ylabel('Number of Tweets', fontsize= 11)
axes[0, 1].set_title('Sentiment Score Distribution', fontsize= 14, fontweight= 'bold', pad= 10)
axes[0, 1].legend()
axes[0, 1].grid(axis= 'y', alpha= 0.3)

# === 3. Content Types (Bar Chart) ===
content_counts= df_analyzed['content_type'].value_counts()
bars= axes[0, 2].bar(content_counts.index, content_counts.values, color= '#e67e22', edgecolor= 'black')
axes[0, 2].set_xlabel('Content Type', fontsize= 11)
axes[0, 2].set_ylabel('Number of Tweets', fontsize= 11)
axes[0, 2].set_title('Content Types', fontsize= 14, fontweight= 'bold', pad= 10)
axes[0, 2].tick_params(axis= 'x', rotation= 45)

for bar in bars:
    height= bar.get_height()
    axes[0, 2].text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha= 'center', va= 'bottom', fontsize= 9)
axes[0, 2].grid(axis= 'y', alpha= 0.3)

# === 4. Top 10 Topics (Horizontal Bar) ===
top_topics= df_analyzed['primary_topic'].value_counts().head(10)
bars= axes[1, 0].barh(range(len(top_topics)), top_topics.values, color= '#9b59b6', edgecolor= 'black')
axes[1, 0].set_yticks(range(len(top_topics)))
axes[1, 0].set_yticklabels(top_topics.index, fontsize= 9)
axes[1, 0].set_xlabel('Number of Tweets', fontsize= 11)
axes[1, 0].set_title('Top 10 Topics', fontsize= 14, fontweight= 'bold', pad= 10)
axes[1, 0].invert_yaxis()

for i, (bar, value) in enumerate(zip(bars, top_topics.values)):
    axes[1, 0].text(value, i, f' {value}', va= 'center', fontsize= 9)
axes[1, 0].grid(axis= 'x', alpha= 0.3)

# === 5. Top Games (Bar Chart) ===
all_games= []
for games_str in df_analyzed['games']:
    try:
        games= eval(games_str)
        all_games.extend(games)
    except:
        pass

if all_games:
    game_counts= Counter(all_games)
    top_games= dict(game_counts.most_common(10))
    bars= axes[1, 1].bar(range(len(top_games)), top_games.values(), color= '#1abc9c', edgecolor= 'black')
    axes[1, 1].set_xticks(range(len(top_games)))
    axes[1, 1].set_xticklabels(top_games.keys(), rotation= 45, ha= 'right', fontsize= 9)
    axes[1, 1].set_ylabel('Mentions', fontsize= 11)
    axes[1, 1].set_title('Top 10 Most Mentioned Games', fontsize= 14, fontweight= 'bold', pad= 10)
    
    for bar in bars:
        height= bar.get_height()
        axes[1, 1].text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha= 'center', va= 'bottom', fontsize= 9)
    axes[1, 1].grid(axis= 'y', alpha= 0.3)
else:
    axes[1, 1].text(0.5, 0.5, 'No games detected', ha= 'center', va= 'center', fontsize= 12)
    axes[1, 1].set_title('Top Games', fontsize= 14, fontweight= 'bold')

# === 6. Top Companies (Bar Chart) ===
all_companies= []
for companies_str in df_analyzed['companies']:
    try:
        companies= eval(companies_str)
        all_companies.extend(companies)
    except:
        pass

if all_companies:
    company_counts= Counter(all_companies)
    top_companies= dict(company_counts.most_common(10))
    bars= axes[1, 2].bar(range(len(top_companies)), top_companies.values(), color= '#e74c3c', edgecolor= 'black')
    axes[1, 2].set_xticks(range(len(top_companies)))
    axes[1, 2].set_xticklabels(top_companies.keys(), rotation= 45, ha= 'right', fontsize= 9)
    axes[1, 2].set_ylabel('Mentions', fontsize= 11)
    axes[1, 2].set_title('Top 10 Most Mentioned Companies', fontsize= 14, fontweight= 'bold', pad= 10)
    
    for bar in bars:
        height= bar.get_height()
        axes[1, 2].text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha= 'center', va= 'bottom', fontsize= 9)
    axes[1, 2].grid(axis= 'y', alpha= 0.3)
else:
    axes[1, 2].text(0.5, 0.5, 'No companies detected', ha= 'center', va= 'center', fontsize= 12)
    axes[1, 2].set_title('Top Companies', fontsize= 14, fontweight= 'bold')

plt.tight_layout()

timestamp= datetime.now().strftime('%Y%m%d_%H%M%S')
filename= f'002_Data/gaming_tweets_dashboard_{timestamp}.png'
plt.savefig(filename, dpi= 300, bbox_inches= 'tight', facecolor= 'white')

print(f"Dashboard saved as: {filename}")
plt.show()


# In[30]:


# Sentiment vs Engagement
fig, ax= plt.subplots(figsize= (10, 6))

sentiment_engagement= df_analyzed.groupby('sentiment')['like_count'].mean().sort_values(ascending= False)

colors_map= {'positive': '#2ecc71', 'neutral': '#95a5a6', 'negative': '#e74c3c'}
colors= [colors_map.get(sent, '#3498db') for sent in sentiment_engagement.index]

bars= ax.bar(sentiment_engagement.index, sentiment_engagement.values, color= colors, edgecolor= 'black', alpha= 0.8)

ax.set_xlabel('Sentiment', fontsize= 12, fontweight= 'bold')
ax.set_ylabel('Average Likes per Tweet', fontsize= 12, fontweight= 'bold')
ax.set_title('Average Engagement by Sentiment\n(Interesting: Negative tweets get slightly more likes)', 
             fontsize= 14, fontweight= 'bold', pad= 15)
ax.grid(axis= 'y', alpha= 0.3)

for bar in bars:
    height= bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f}', ha= 'center', va= 'bottom', fontsize= 11, fontweight= 'bold')

plt.tight_layout()

filename2= f'002_Data/sentiment_engagement_{timestamp}.png'
plt.savefig(filename2, dpi= 300, bbox_inches= 'tight', facecolor= 'white')
print(f"Engagement chart saved as: {filename2}")
plt.show()


# In[31]:


print(f"\nAnalysis Summary:")
print(f"Total tweets analyzed: {len(df_analyzed)}")
print(f"Overall sentiment: {'Positive' if avg_sentiment > 0.6 else 'Neutral' if avg_sentiment > 0.4 else 'Negative'}")
print(f"Average sentiment score: {avg_sentiment:.2f}/1.00")
print(f"Unique games detected: {len(game_counts)}")
print(f"Unique companies detected: {len(company_counts)}")
print(f"Unique platforms detected: {len(platform_counts)}")

print(f"\nKey Insights:")
print(f"Most discussed topic: {top_topics.index[0]}")
print(f"Most mentioned game: {list(game_counts.most_common(1)[0])[0] if game_counts else 'N/A'}")
print(f"Most mentioned company: {list(company_counts.most_common(1)[0])[0] if company_counts else 'N/A'}")
print(f"Dominant content type: {content_counts.index[0]}")

print(f"\nFiles created:")
print(f"Dashboard: gaming_tweets_dashboard_{timestamp}.png")
print(f"Engagement chart: sentiment_engagement_{timestamp}.png")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




