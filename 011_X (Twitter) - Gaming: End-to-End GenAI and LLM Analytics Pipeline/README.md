# X (Twitter)- Gaming🎮: End-to-End GenAI and LLM Analytics Pipeline

## 📊 Project Overview

This project demonstrates an **End-to-End Data Analytics Pipeline** that collects gaming tweets from X (Twitter), enriches them with **AI-powered Sentiment Analysis using Anthropic's Claude Sonnet 4.5** and generates actionable insights through **Visualizations and Dashboards**.

The pipeline processes **100 gaming community tweets** through a 3-stage workflow: **Data Collection**, **GenAI improvement with Large Language Models (LLMs)** and **Exploratory Data Analysis with Visualization**. The project showcases modern data engineering practices, GenAI integration, entity extraction (games, companies, platforms), and multi-dimensional sentiment analysis.

Using **Claude Sonnet 4.5 LLM**, the pipeline achieved comprehensive **Sentiment Classification (61% positive, 25% neutral, 14% negative)** with an **Avg Sentiment score of 0.64/1.00**, while successfully extracting **38 unique games, 53 companies, and 35 platforms** from the gaming discourse.

---

## 🎯 Key Objectives

- **Data Engineering Practice:**
  - Build automated tweet collection pipeline from X API
  - Implement secure API authentication with environment variables
  - Design modular, reusable code architecture (`Src/` modules)
  - Handle rate limiting and error management

- **GenAI & LLM Application:**
  - Integrate Anthropic Claude Sonnet 4.5 API for natural language understanding
  - Engineer effective prompts for consistent structured outputs
  - Extract multi-dimensional insights (sentiment, topics, entities)
  - Process 100 tweets with AI enrichment (~$1 cost)

- **Data Analytics:**
  - Perform comprehensive exploratory data analysis (EDA)
  - Generate professional multi-chart visualizations
  - Identify patterns and correlations in gaming community sentiment
  - Extract actionable business insights from AI-enriched data

---

## 📁 Project Structure
```
📁 X (Twitter)- Gaming🎮: End-to-End GenAI and LLM Analytics Pipeline/
│
├── 📓 001_tweet_collector.ipynb
├── 📓 002_ai_claude_sentiment_analysis.ipynb
├── 📓 003_data_exploration_visualisation.ipynb
│
├── 📁 Src/
│   ├── 📄 claude_analyzer.py
│   └── 📓 claude_analyzer.ipynb
│
└── 📁 002_Data/
    ├── 📊 gaming_tweets_20251218_142234.csv
    ├── 📊 gaming_tweets_analyzed_20260110_122738.csv
    ├── 📈 gaming_tweets_dashboard_20260112_141740.png
    └── 📈 sentiment_engagement_20260112_141740.png
```

---

## 📈 Key Findings

**Sentiment Distribution:**
- **61% Positive sentiment** - Gaming community leans positive overall
- **Average score: 0.64/1.00** - Moderately positive community mood
- **Most positive:** Nintendo/Square Enix collaboration mention (0.90 score)
- **Most negative:** NVIDIA graphics card criticism (0.10 score)

**Trending Topics:**
- **Blockchain gaming** dominates discussions (6 tweets - #1 topic)
- **Crypto/Web3 integration** emerging trend (4 tweets)
- Traditional gaming content remains strong

**Entity Extraction:**
- **38 unique games** detected (GTA 6 most mentioned with 3 mentions)
- **53 unique companies** identified (LEGAS, NVIDIA, Nintendo lead)
- **35 unique platforms** found (PC, PS5, YouTube dominant)

**Engagement Paradox:**
- **Negative tweets receive 5% more engagement** (0.21 vs 0.20 avg likes)
- Controversy and complaints drive more community interaction than positive content

**Content Distribution:**
- Discussion (30%) and Excitement (26%) dominate content types
- Complaints constitute 12% - moderate criticism level

---

## 📊 Results Summary

| Metric | Value |
|--------|-------|
| **Total Tweets Analyzed** | 100 |
| **Processing Time** | 7.02 minutes |
| **AI Cost** | ~$1.00 (Claude Sonnet 4.5) |
| **Data Columns (Raw)** | 8 columns |
| **Data Columns (Enriched)** | 19 columns |
| **Overall Sentiment** | 61% Positive |
| **Avg Sentiment Score** | 0.64 / 1.00 |
| **Unique Games Detected** | 38 games |
| **Unique Companies** | 53 companies |
| **Unique Platforms** | 35 platforms |
| **Top Game** | GTA 6 (3 mentions) |
| **Top Company** | LEGAS (4 mentions) |
| **Trending Topic** | Blockchain gaming (6 tweets) |
| **Dominant Content Type** | Discussion (30%) |

---

## 🔄 Process

### 1. Data Collection & Engineering

**API Setup:**
- Configured X (Twitter) API authentication with Bearer Token
- Implemented secure credential management using `.env` file
- Set up python-dotenv for environment variable loading

**Data Pipeline:**
- Built automated collection system for gaming-related tweets
- Filtered for English language content
- Applied search criteria: gaming keywords, recent tweets
- Extracted engagement metrics: likes, retweets, replies, quotes

**Feature Extraction:**
- Parsed 8 core features per tweet:
  - Tweet metadata: `tweet_id`, `text`, `created_at`, `author_id`
  - Engagement: `retweet_count`, `reply_count`, `like_count`, `quote_count`

**Data Storage:**
- Saved structured dataset to CSV (100 tweets × 8 features)
- Timestamped filename for version tracking

### 2. GenAI Enrichment with Claude LLM

**API Integration:**
- Authenticated with Anthropic Claude API (Sonnet 4.5 model)
- Implemented rate limiting (0.5s delay between requests)
- Built robust error handling (JSON parsing errors, API failures)

**Prompt Engineering:**
- Designed structured prompt for consistent JSON outputs
- Specified exact schema for sentiment, topics, entities, content type
- Requested no markdown, pure JSON responses

**AI Analysis per Tweet:**
- **Sentiment Analysis:**
  - Classification: Positive/Negative/Neutral
  - Confidence score: 0.0 (very negative) to 1.0 (very positive)
- **Topic Extraction:**
  - Primary topic (2-3 words)
  - Related topics list
- **Entity Recognition:**
  - Games: Automatic game title detection
  - Companies: Publisher/developer identification
  - Platforms: PC, console, mobile extraction
  - People: Influencer mentions
- **Content Classification:**
  - 7 types: complaint, excitement, question, news, review, discussion, other
- **AI Summary:**
  - One-sentence summary per tweet

**Data Enrichment:**
- Added 11 new AI-generated columns to dataset
- Converted list objects to strings for CSV storage
- Added `analyzed_at` timestamp for each analysis

**Output:**
- Saved enriched dataset to CSV (100 tweets × 19 features)
- Processing time: 7.02 minutes
- Cost: ~$1.00 for 100 tweets

### 3. Exploratory Data Analysis (EDA)

**Sentiment Analysis:**
- Calculated sentiment distribution across positive/neutral/negative
- Computed average sentiment score (0.64/1.00)
- Identified most positive and most negative tweets
- Analyzed sentiment score distribution (histogram)

**Topic Exploration:**
- Ranked top 10 primary topics by frequency
- Identified trending themes (blockchain gaming, crypto trading)
- Categorized content types (discussion, excitement, complaints)

**Entity Extraction:**
- Counted unique games, companies, platforms, people
- Ranked most mentioned entities
- GTA 6, LEGAS, PC identified as top entities

**Engagement Analysis:**
- Calculated total and average engagement metrics
- Analyzed sentiment correlation with engagement
- Discovered negative tweets receive more likes (0.21 vs 0.20)

**Correlation Analysis:**
- Examined sentiment vs engagement patterns
- Identified content type impact on engagement
- Found controversy drives interaction

### 4. Data Visualization

**6-Panel Dashboard:**
1. **Sentiment Distribution** (Pie Chart)

2. **Sentiment Scores** (Histogram)

3. **Content Types** (Bar Chart)

4. **Top 10 Topics** (Horizontal Bar)

5. **Most Mentioned Games** (Bar Chart)

6. **Top Companies** (Bar Chart)

**Additional Visualizations:**
- **Sentiment vs Engagement** analysis chart

---

## 💻 Technologies Used

**Data Engineering & APIs:**
- **Python:** requests, json, os
- **API Integration:** X (Twitter) API v2, Anthropic Claude API
- **Rate Limiting:** Custom time.sleep() implementation
- **Security:** python-dotenv for environment variable management
- **Error Handling:** Try-except blocks, JSON validation

**Data Processing & Analysis:**
- **Python:** Pandas, NumPy
- **Data Cleaning:** Type conversions, string-to-list parsing
- **Feature Engineering:** AI-generated features (sentiment, topics, entities)
- **Data Structures:** Collections.Counter for entity counting

**GenAI & LLMs:**
- **Model:** Claude Sonnet 4.5 (`claude-sonnet-4-20250514`)
- **Framework:** Anthropic Python SDK
- **Prompt Engineering:** Structured JSON output prompts
- **NLP Tasks:**
  - Sentiment analysis
  - Topic extraction
  - Named Entity Recognition (NER)
  - Content classification
  - Text summarization

**Data Visualization:**
- **Python:** Matplotlib, Seaborn
- **Chart Types:** Pie, histogram, bar, horizontal bar
- **Styling:** Custom colors, gridlines, value labels
- **Export:** High-resolution PNG (300 DPI)

**Development Tools:**
- **IDE:** Jupyter Notebook
- **Version Control:** Git, GitHub
- **Architecture:** Modular design (`Src/` folder)


