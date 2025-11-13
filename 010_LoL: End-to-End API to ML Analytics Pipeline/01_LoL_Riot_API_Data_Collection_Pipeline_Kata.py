#!/usr/bin/env python
# coding: utf-8

# ### Import the Basic Libraries 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# --- Or import the libraries from mine py ---

# In[2]:


import sys
sys.path.append(r'C:\Users\User\005_Libraries')

import mylibs


# In[3]:


import requests
import urllib.parse
import json
import time
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()


# ### Set Up the API Key

# In[4]:


API_KEY= os.getenv('RIOT_API_KEY')
REGION= os.getenv('RIOT_REGION', 'euw1')

BASE_URL= f"https://{REGION}.api.riotgames.com"
EUROPE_URL= "https://europe.api.riotgames.com"

HEADERS= {"X-Riot-Token": API_KEY}


# ### Call & Test API

# In[5]:


def get_player_data(game_name, tag_line):
    """
    Get complete player data using Riot ID (GameName#TagLine)
    
    Parameters:
    - game_name: Your game name (e.g., "MpampoKilleRR")
    - tag_line: Your tag (e.g., "EUW")
    
    Returns:
    - Dictionary with all player data
    """
    print(f"\n{'='*60}")
    print(f"Looking up player: {game_name}#{tag_line}")
    print('='*60)
    
    account_url= f"{EUROPE_URL}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    
    try:
        account_response= requests.get(account_url, headers= HEADERS)
        
        if account_response.status_code== 200:
            account_data= account_response.json()
            print(f"Account found: {account_data['gameName']}#{account_data['tagLine']}")
        else:
            print(f"Account not found: {account_response.status_code}")
            return None
    
    except Exception as e:
        print(f"Error getting account: {e}")
        return None
    
    puuid= account_data['puuid']
    summoner_url= f"{BASE_URL}/lol/summoner/v4/summoners/by-puuid/{puuid}"
    
    try:
        summoner_response= requests.get(summoner_url, headers= HEADERS)
        
        if summoner_response.status_code== 200:
            summoner_data= summoner_response.json()
            print(f"Summoner data retrieved!")
        else:
            print(f"Failed to get summoner data: {summoner_response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error getting summoner: {e}")
        return None
    
    player_data= {
        'gameName': account_data['gameName'],
        'tagLine': account_data['tagLine'],
        'puuid': account_data['puuid'],
        'summonerLevel': summoner_data['summonerLevel'],
        'profileIconId': summoner_data['profileIconId'],
        'revisionDate': summoner_data.get('revisionDate')
    }
    
    print(f"\n Player Summary:")
    print(f"   Player: {player_data['gameName']}#{player_data['tagLine']}")
    print(f"   Level: {player_data['summonerLevel']}")
    print(f"   Profile Icon: {player_data['profileIconId']}")
    print(f"   PUUID: {player_data['puuid']}")
    
    return player_data


# get_player_data("MpampoKilleRR", "EUW")

# In[6]:


my_player= get_player_data("MpampoKilleRR", "EUW")

if my_player:
    print("\n" + "="*60)
    print("YOUR LEAGUE ACCOUNT DATA:")
    print("="*60)
    for key, value in my_player.items():
        print(f"   {key}: {value}")


# ### Fetch Match History

# In[7]:


def get_match_history(puuid, count= 20):
    """
    Get list of recent match IDs for a player
    
    Parameters:
    - puuid: Player's PUUID (the permanent unique ID)
    - count: Number of matches to retrieve (default 20, max 100)
    
    Returns:
    - List of match IDs
    """
    print(f"\n{'='*60}")
    print(f"Fetching last {count} matches")
    print('='*60)
    
    matches_url= f"{EUROPE_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids"
    
    params= {
        'start': 0,
        'count': count
    }
    
    try:
        response= requests.get(matches_url, headers= HEADERS, params= params)
        
        if response.status_code== 200:
            match_ids= response.json()
            print(f"Retrieved {len(match_ids)} matches!")
            
            print(f"\n First 3 match IDs:")
            for i, match_id in enumerate(match_ids[:3], 1):
                print(f"   {i}. {match_id}")
            print(f"   ... and {len(match_ids) - 3} more")
            
            return match_ids
        else:
            print(f"Failed to get matches: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None


# In[8]:


get_match_history(my_player['puuid'], count= 20)


# In[9]:


if my_player:
    my_matches= get_match_history(my_player['puuid'], count= 20)
    
    if my_matches:
        print(f"\n{'='*60}")
        print(f"YOUR RECENT MATCHES:")
        print('='*60)
        print(f"Total matches retrieved: {len(my_matches)}")
        
        print(f"\n All Match IDs:")
        for i, match_id in enumerate(my_matches, 1):
            print(f"   {i}. {match_id}")


# In[10]:


def count_total_matches(puuid, max_check= 10000):
    """
    Estimate total number of available matches
    (API doesn't give us a total count directly)
    """
    print(f"\n{'='*60}")
    print(f"Checking total matches available...")
    print('='*60)
    
    matches_url= f"{EUROPE_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids"
    
    all_matches= []
    start= 0
    count= 100
    
    while start < max_check:
        params= {
            'start': start,
            'count': count
        }
        
        try:
            response= requests.get(matches_url, headers= HEADERS, params= params)
            
            if response.status_code== 200:
                match_batch= response.json()
                
                if len(match_batch)== 0:
                    break
                
                all_matches.extend(match_batch)
                print(f"   Retrieved {len(match_batch)} matches (Total so far: {len(all_matches)})")
                
                start += count
                time.sleep(0.5)
            else:
                print(f"Error: {response.status_code}")
                break
                
        except Exception as e:
            print(f"Error: {e}")
            break
    
    print(f"\n Total matches found: {len(all_matches)}")
    return all_matches


# In[11]:


count_total_matches(my_player['puuid'], max_check= 10000)


# ### Get Detailed Match Data

# In[12]:


def get_match_details(match_id):
    """
    Get detailed information about a specific match
    
    Parameters:
    - match_id: The match ID (e.g., 'EUW1_7583720465')
    
    Returns:
    - Dictionary with all match data
    """
    match_url= f"{EUROPE_URL}/lol/match/v5/matches/{match_id}"
    
    try:
        response= requests.get(match_url, headers= HEADERS)
        
        if response.status_code== 200:
            match_data= response.json()
            return match_data
        else:
            print(f"Failed to get match {match_id}: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error getting match {match_id}: {e}")
        return None


# In[13]:


get_match_details('EUW1_7583720465')


# In[14]:


if my_matches:
    print(f"\n{'='*60}")
    print(f"GETTING DETAILED DATA FOR FIRST MATCH")
    print('='*60)
    
    first_match_id= my_matches[0]
    print(f"Match ID: {first_match_id}")
    
    match_details = get_match_details(first_match_id)
    
    if match_details:
        print(f"\n Match data retrieved!")
        
        print(f"\nMatch Data Structure:")
        print(f"Top-level keys: {list(match_details.keys())}")
        
        info= match_details['metadata']
        print(f"\n Match Metadata:")
        print(f"   Match ID: {info['matchId']}")
        print(f"   Participants: {len(info['participants'])} players")
        
        game_info= match_details['info']
        print(f"\n Game Info:")
        print(f"   Game Mode: {game_info['gameMode']}")
        print(f"   Game Duration: {game_info['gameDuration'] // 60} minutes {game_info['gameDuration'] % 60} seconds")
        print(f"   Game Version: {game_info['gameVersion']}")
        
        participants= game_info['participants']
        your_puuid= my_player['puuid']
        
        for player in participants:
            if player['puuid']== your_puuid:
                print(f"\n YOUR PERFORMANCE:")
                print(f"   Champion: {player['championName']}")
                print(f"   KDA: {player['kills']}/{player['deaths']}/{player['assists']}")
                print(f"   Win: {'Victory' if player['win'] else 'Defeat'}")
                print(f"   Gold Earned: {player['goldEarned']:,}")
                print(f"   Total Damage to Champions: {player['totalDamageDealtToChampions']:,}")
                break


# ### Test With Katarina + CLASSIC

# In[15]:


def count_katarina_games(puuid, total_matches= 100):
    """
    Count how many Katarina games in CLASSIC mode we have
    
    Parameters:
    - puuid: My PUUID
    - total_matches: How many matches to check (default 100)
    
    Returns:
    - Number of Katarina CLASSIC games found
    """
    print(f"\n{'='*60}")
    print(f"Analyzing my matches for Katarina games...")
    print('='*60)
    
    matches_url= f"{EUROPE_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params= {
            'start': 0, 
            'count': total_matches
            }
    
    try:
        response= requests.get(matches_url, headers= HEADERS, params= params)
        if response.status_code != 200:
            print(f"Error getting matches: {response.status_code}")
            return 0
        
        match_ids= response.json()
        print(f"Retrieved {len(match_ids)} match IDs")
        
    except Exception as e:
        print(f"Error: {e}")
        return 0
    
    katarina_count= 0
    other_modes_count= 0
    other_champs_count= 0
    
    print(f"\n Checking each match...")
    
    for i, match_id in enumerate(match_ids):
        match_data= get_match_details(match_id)
        
        if not match_data:
            continue
        
        game_info= match_data['info']
        game_mode= game_info['gameMode']
        
        for player in game_info['participants']:
            if player['puuid']== puuid:
                champion= player['championName']
                
                if champion== 'Katarina' and game_mode== 'CLASSIC':
                    katarina_count += 1
                    print(f"Match {i+1}/{len(match_ids)}: Katarina CLASSIC (Total: {katarina_count})")
                elif champion== 'Katarina' and game_mode != 'CLASSIC':
                    other_modes_count += 1
                    print(f"Match {i+1}/{len(match_ids)}: Katarina {game_mode}")
                else:
                    other_champs_count += 1
                    print(f"Match {i+1}/{len(match_ids)}: {champion} {game_mode}")
                break
        
        time.sleep(0.6)
    
    print(f"\n {'='*60}")
    print(f"RESULTS:")
    print('='*60)
    print(f"   Katarina CLASSIC games: {katarina_count}")
    print(f"   Katarina other modes: {other_modes_count}")
    print(f"   Other champions: {other_champs_count}")
    print(f"   Total checked: {len(match_ids)}")
    
    return katarina_count


# ### Test With my First 100 Matches

# In[16]:


katarina_games= count_katarina_games(my_player['puuid'], total_matches= 100)

print(f"\n Found {katarina_games} Katarina CLASSIC games in my last 100 matches!")


# ### Data Collection Pipeline

# In[17]:


def extract_katarina_match_data(match_data, your_puuid):
    """
    Extract all relevant features (21) from Katarina CLASSIC match
    
    Parameters:
    - match_data: Full match data from API
    - your_puuid: Your PUUID to identify your stats
    
    Returns:
    - Dictionary with all features, or None if not Katarina CLASSIC
    """
    game_info= match_data['info']
    
    # Check if it's CLASSIC mode
    if game_info['gameMode'] != 'CLASSIC':
        return None
    
    # Find your stats and your team
    your_stats= None
    your_team_id= None
    
    # Check if you played Katarina
    for player in game_info['participants']:
        if player['puuid'] == your_puuid:
            if player['championName'] != 'Katarina':
                return None
            
            your_stats= player
            your_team_id= player['teamId']
            break
    
    if not your_stats:
        return None
    
    # Calculate team totals (kills and deaths)
    team_kills= 0
    team_deaths= 0
    
    for player in game_info['participants']:
        if player['teamId'] == your_team_id:
            team_kills += player['kills']
            team_deaths += player['deaths']
    
    # Get team objectives
    team_objectives = None
    for team in game_info['teams']:
        if team['teamId'] == your_team_id:
            team_objectives = team['objectives']
            break
    
    # Extract game duration (in seconds)
    game_duration= game_info['gameDuration']
    game_duration_min= game_duration / 60
    
    # Extract YOUR performance stats
    kills= your_stats['kills']
    deaths= your_stats['deaths']
    assists= your_stats['assists']
    cs= your_stats['totalMinionsKilled'] + your_stats.get('neutralMinionsKilled', 0)
    gold_earned= your_stats['goldEarned']
    damage_to_champions= your_stats['totalDamageDealtToChampions']
    damage_taken= your_stats['totalDamageTaken']
    level= your_stats['champLevel']
    win= your_stats['win']
    
    # Extract team objectives
    team_dragons= team_objectives['dragon']['kills']
    team_barons= team_objectives['baron']['kills']
    team_towers= team_objectives['tower']['kills']
    first_blood= team_objectives['champion']['first']
    
    # Calculated features
    # KDA ratio (handle deaths= 0)
    if deaths == 0:
        kda_ratio= kills + assists 
    else:
        kda_ratio= (kills + assists) / deaths
    
    # Per minute stats
    cs_per_min= cs / game_duration_min
    gold_per_min= gold_earned / game_duration_min
    damage_per_min= damage_to_champions / game_duration_min
    
    # Participation and share stats
    # Kill participation (handle team_kills= 0)
    if team_kills == 0:
        kill_participation= 0
        kill_share= 0
    else:
        kill_participation= (kills + assists) / team_kills
        kill_share= kills / team_kills
    
    # Death share (handle team_deaths= 0)
    if team_deaths == 0:
        death_share= 0
    else:
        death_share= deaths / team_deaths
    
    # Return all features as a dictionary
    return {
        # Match info
        'game_duration': game_duration,
        'win': 1 if win else 0,
        
        # Your performance
        'kills': kills,
        'deaths': deaths,
        'assists': assists,
        'cs': cs,
        'gold_earned': gold_earned,
        'damage_to_champions': damage_to_champions,
        'damage_taken': damage_taken,
        'level': level,
        
        # Team performance
        'team_dragons': team_dragons,
        'team_barons': team_barons,
        'team_towers': team_towers,
        'first_blood': 1 if first_blood else 0,
        
        # Calculated features
        'kda_ratio': round(kda_ratio, 2),
        'cs_per_min': round(cs_per_min, 2),
        'gold_per_min': round(gold_per_min, 2),
        'damage_per_min': round(damage_per_min, 2),
        'kill_participation': round(kill_participation, 3),
        'kill_share': round(kill_share, 3),
        'death_share': round(death_share, 3)
    }


# ### Data Collection Function

# In[18]:


def collect_katarina_dataset(puuid, num_matches= 1000):
    """
    Collect complete dataset of Katarina CLASSIC matches
    Handles API limit of 100 matches per request by batching
    
    Parameters:
    - puuid: Your PUUID
    - num_matches: Total number of matches to check (will batch in groups of 100)
    
    Returns:
    - pandas DataFrame with all Katarina match data
    """
    print(f"\n {'='*60}")
    print(f"COLLECTING KATARINA DATASET")
    print('='*60)
    print(f"Target: Check last {num_matches} matches...")
    
    # API limit is 100 matches per request
    batch_size= 100
    all_match_ids= []
    
    # Calculate number of batches needed
    num_batches= (num_matches + batch_size - 1) // batch_size
    
    print(f"Will make {num_batches} API requests (batches of {batch_size})\n")
    
    # Get match IDs in batches
    for batch_num in range(num_batches):
        start= batch_num * batch_size
        count= min(batch_size, num_matches - start)
        
        matches_url= f"{EUROPE_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params= {'start': start, 'count': count}
        
        print(f"Batch {batch_num + 1}/{num_batches}: Fetching matches {start} to {start + count - 1}...")
        
        try:
            response= requests.get(matches_url, headers= HEADERS, params= params)
            
            if response.status_code == 200:
                batch_ids= response.json()
                all_match_ids.extend(batch_ids)
                print(f"Retrieved {len(batch_ids)} match IDs (Total so far: {len(all_match_ids)})")
            else:
                print(f"Error {response.status_code}: {response.text}")
                break
                
        except Exception as e:
            print(f"Error: {e}")
            break
        
        # Rate limiting between batches
        if batch_num < num_batches - 1:
            time.sleep(1)
    
    if not all_match_ids:
        print("\n No match IDs retrieved!")
        return None
    
    print(f"\n Total match IDs retrieved: {len(all_match_ids)}")
    
    # Collect data for each match
    all_matches_data= []
    katarina_count= 0
    
    print(f"\n {'='*60}")
    print(f"PROCESSING MATCHES FOR KATARINA GAMES")
    print(f"{'='*60}\n")
    
    # Get match details
    for i, match_id in enumerate(all_match_ids):
        match_data= get_match_details(match_id)
        
        if not match_data:
            print(f"Match {i+1}/{len(all_match_ids)}: Failed to retrieve")
            continue
        
        # Extract Katarina data
        kat_data= extract_katarina_match_data(match_data, puuid)
        
        if kat_data:
            all_matches_data.append(kat_data)
            katarina_count += 1
            result= "WIN" if kat_data['win'] == 1 else "LOSS"
            kda= f"{kat_data['kills']}/{kat_data['deaths']}/{kat_data['assists']}"
            print(f"Match {i+1}/{len(all_match_ids)}: Katarina {result} | KDA: {kda} | Total Kat games: {katarina_count}")
        else:
            print(f"Match {i+1}/{len(all_match_ids)}: Skipped (not Katarina CLASSIC)")
        
        # Rate limiting
        time.sleep(1.5)
    
    # Convert to DataFrame
    if not all_matches_data:
        print("\n No Katarina games found!")
        return None
    
    df= pd.DataFrame(all_matches_data)
    
    print(f"\n {'='*60}")
    print(f"DATA COLLECTION COMPLETE!")
    print('='*60)
    print(f"   Total matches checked: {len(all_match_ids)}")
    print(f"   Katarina CLASSIC games found: {len(df)}")
    print(f"   Features collected: {len(df.columns)}")
    print(f"   Dataset shape: {df.shape}")
    
    return df


# ### Collect the Data & Save in CSV

# In[21]:


# Collect 1000 matches (will make 10 API requests for match IDs)

katarina_df= collect_katarina_dataset(my_player['puuid'], num_matches= 1000)

# Display results
if katarina_df is not None:
    print(f"\n {'='*60}")
    print(f"DATASET PREVIEW:")
    print('='*60)
    print(katarina_df.head(10))
    
    print(f"\n {'='*60}")
    print(f"DATASET INFO:")
    print('='*60)
    print(katarina_df.info())
    
    print(f"\n {'='*60}")
    print(f"BASIC STATISTICS:")
    print('='*60)
    print(katarina_df.describe())
    
    # Save to CSV
    katarina_classic= 'katarina_matches_1000.csv'
    katarina_df.to_csv(katarina_classic, index= False)
    print(f"\n Dataset saved to: {katarina_classic}")


# In[22]:


df_kata= pd.read_csv(katarina_classic)
df_kata


# In[23]:


df_kata.info()


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





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




