#!/usr/bin/env python
# coding: utf-8

# ### Claude AI Tweet Analyzer

# In[1]:


"""
Claude AI Tweet Analyzer
Providesthe function for analyzing tweets using Anthropic's Claude API
"""

import anthropic
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def analyze_tweet(tweet_text):
    """
    Analyze a gaming tweet with Claude AI
    
    Args:
        tweet_text (str): The tweet text to analyze
        
    Returns:
        dict: Analysis with sentiment, topics, entities
    """
    
    claude_api_key= os.getenv('ANTHROPIC_API_KEY')
    client= anthropic.Anthropic(api_key= claude_api_key)
    
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
                        "content": prompt}]
        )
        
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


# In[ ]:




