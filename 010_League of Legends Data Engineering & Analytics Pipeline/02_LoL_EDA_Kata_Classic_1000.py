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


# In[ ]:





# ### Katarina (df_kata) Dataset Overview 

# In[3]:


katarina_classic= 'katarina_matches_1000.csv'
df_kata= pd.read_csv(katarina_classic)
df_kata


# In[4]:


df_kata.info()


# In[5]:


df_kata.dtypes


# In[6]:


df_kata.describe().transpose()


# In[7]:


df_kata.isnull().sum()


# In[8]:


df_kata.head()


# In[9]:


df_kata.tail()


# In[ ]:





# ### Win Rate

# In[10]:


print(f"\n {'='*60}")
print("WIN RATE ANALYSIS")
print("="*60)

# Calculate win rate
wins= df_kata['win'].sum()
losses= len(df_kata) - wins
total= len(df_kata)
win_rate= (wins / total) * 100
loss_rate= (losses / total) * 100

print(f"Total Games: {total}")
print(f"Total Wins: {wins}")
print(f"Total Losses: {losses}")
print(f"Win Rate: {win_rate:.2f}%")
print(f"Loss Rate: {loss_rate:.2f}%")

# Create visualizations
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Katarina Win Rate Analysis', fontsize= 16, fontweight= 'bold', y= 1.02)

# 1. Pie chart
colors= ['#4CAF50', '#F44336']
explode= (0.05, 0)
axes[0].pie([wins, losses], 
            labels= ['Wins', 'Losses'], 
            autopct= '%1.1f%%', 
            colors= colors,
            explode= explode,
            startangle= 90,
            textprops= {'fontsize': 12, 'fontweight': 'bold'})
axes[0].set_title('Win/Loss Distribution', fontsize= 14, fontweight= 'bold')

# 2. Bar chart
bars= axes[1].bar(['Wins', 'Losses'], [wins, losses], color= colors, alpha= 0.8, edgecolor= 'black', linewidth= 2)
axes[1].set_ylabel('Number of Games', fontsize= 12, fontweight= 'bold')
axes[1].set_title('Win vs Loss Count', fontsize= 14, fontweight= 'bold')
axes[1].grid(axis= 'y', alpha= 0.3)

# Add value labels on bars
for bar in bars:
    height= bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha= 'center', va= 'bottom', fontsize= 14, fontweight= 'bold')

# 3. Win rate gauge (horizontal bar)
axes[2].barh(['Win Rate'], [win_rate], color= '#4CAF50', alpha= 0.8, edgecolor= 'black', linewidth= 2)
axes[2].barh(['Win Rate'], [100], color= 'lightgray', alpha= 0.3)
axes[2].set_xlim(0, 100)
axes[2].set_xlabel('Percentage (%)', fontsize= 12, fontweight= 'bold')
axes[2].set_title('Win Rate Percentage', fontsize= 14, fontweight= 'bold')
axes[2].text(win_rate/2, 0, f'{win_rate:.1f}%', 
            ha= 'center', va= 'center', fontsize= 16, fontweight= 'bold', color= 'white')
axes[2].grid(axis= 'x', alpha= 0.3)

plt.tight_layout()
plt.show()

print(f"\n {'='*60}")
print("EXPLANATION:")
print("="*60)
if win_rate > 50:
    print(f"You have a POSITIVE win rate! ({win_rate:.1f}%)")
    print(f"You win more games than you lose with Katarina!")
elif win_rate == 50:
    print(f"You have a BALANCED win rate (50%)")
else:
    print(f"You have a NEGATIVE win rate ({win_rate:.1f}%)")
    print(f"Room for improvement!")


# ### Wins vs Losses

# In[11]:


# Separate wins and losses
wins_df= df_kata[df_kata['win']== 1]
losses_df= df_kata[df_kata['win']== 0]

print(f"\n Wins: {len(wins_df)} games")
print(f" Losses: {len(losses_df)} games")

# Select key stats to compare
comparison_stats= ['kills', 'deaths', 'assists', 'kda_ratio', 
                   'cs', 'cs_per_min', 'gold_per_min', 'damage_per_min',
                   'team_dragons', 'team_barons', 'team_towers']

# Create comparison DataFrame
comparison= pd.DataFrame({
    'Wins_Avg': wins_df[comparison_stats].mean().round(),
    'Losses_Avg': losses_df[comparison_stats].mean().round(),
})
comparison['Difference']= comparison['Wins_Avg'] - comparison['Losses_Avg']
comparison['% Difference']= (comparison['Difference'] / comparison['Losses_Avg'] * 100).round(1)

# Sort by absolute difference
comparison= comparison.sort_values('Difference', ascending= False, key= abs)

print(f"\n {'='*60}")
print("KEY STATS COMPARISON:")
print("="*60)
print(comparison)


# ### KDA Distribution Analysis

# In[12]:


# Overall KDA stats
print(f"\n OVERALL KDA STATISTICS:")
print(f"   Average KDA: {df_kata['kda_ratio'].mean():.2f}")
print(f"   Median KDA: {df_kata['kda_ratio'].median():.2f}")
print(f"   Best KDA: {df_kata['kda_ratio'].max():.2f}")
print(f"   Worst KDA: {df_kata['kda_ratio'].min():.2f}")
print(f"   Std Dev: {df_kata['kda_ratio'].std():.2f}")

# KDA in wins vs losses
print(f"\n KDA IN WINS vs LOSSES:")
print(f"   Wins - Average KDA: {wins_df['kda_ratio'].mean():.2f}")
print(f"   Wins - Median KDA: {wins_df['kda_ratio'].median():.2f}")
print(f"   Losses - Average KDA: {losses_df['kda_ratio'].mean():.2f}")
print(f"   Losses - Median KDA: {losses_df['kda_ratio'].median():.2f}")

# Kills, Deaths, Assists breakdown
print(f"\n KILLS/DEATHS/ASSISTS BREAKDOWN:")
print(f"\n KILLS:")
print(f"   Overall: {df_kata['kills'].mean():.1f}")
print(f"   Wins: {wins_df['kills'].mean():.1f}")
print(f"   Losses: {losses_df['kills'].mean():.1f}")

print(f"\n DEATHS:")
print(f"   Overall: {df_kata['deaths'].mean():.1f}")
print(f"   Wins: {wins_df['deaths'].mean():.1f}")
print(f"   Losses: {losses_df['deaths'].mean():.1f}")

print(f"\n ASSISTS:")
print(f"   Overall: {df_kata['assists'].mean():.1f}")
print(f"   Wins: {wins_df['assists'].mean():.1f}")
print(f"   Losses: {losses_df['assists'].mean():.1f}")

# KDA categories
print(f"\n {'='*60}")
print("KDA PERFORMANCE CATEGORIES:")
print("="*60)

# Define KDA categories
def kda_category(kda):
    if kda >= 10:
        return 'Legendary (10+)'
    elif kda >= 5:
        return 'Great (5-10)'
    elif kda >= 3:
        return 'Good (3-5)'
    elif kda >= 2:
        return 'Average (2-3)'
    else:
        return 'Poor (<2)'

df_kata['kda_category']= df_kata['kda_ratio'].apply(kda_category)

kda_dist= df_kata['kda_category'].value_counts().sort_index()
print(f"\n {kda_dist}")

# Win rate by KDA category
print(f"\n {'='*60}")
print("WIN RATE BY KDA CATEGORY:")
print("="*60)

for category in ['Poor (<2)', 'Average (2-3)', 'Good (3-5)', 'Great (5-10)', 'Legendary (10+)']:
    if category in df_kata['kda_category'].values:
        category_games= df_kata[df_kata['kda_category']== category]
        win_rate= (category_games['win'].sum() / len(category_games) * 100)
        print(f"{category}: {win_rate:.1f}% win rate ({len(category_games)} games)")

# Visualize KDA distributions
fig, axes= plt.subplots(2, 2, figsize= (14, 10))
fig.suptitle('KDA Distribution Analysis', fontsize= 16, fontweight= 'bold')

# 1. Overall KDA histogram
axes[0, 0].hist(df_kata['kda_ratio'], bins= 20, color= '#2196F3', alpha= 0.7, edgecolor= 'black')
axes[0, 0].axvline(df_kata['kda_ratio'].mean(), color= 'red', linestyle='--', linewidth= 2, 
                   label= f'Mean: {df_kata["kda_ratio"].mean():.2f}')
axes[0, 0].axvline(df_kata['kda_ratio'].median(), color= 'green', linestyle= '--', linewidth= 2,
                   label= f'Median: {df_kata["kda_ratio"].median():.2f}')
axes[0, 0].set_xlabel('KDA Ratio', fontsize= 12, fontweight= 'bold')
axes[0, 0].set_ylabel('Frequency', fontsize= 12, fontweight= 'bold')
axes[0, 0].set_title('Overall KDA Distribution', fontsize= 13, fontweight= 'bold')
axes[0, 0].legend()
axes[0, 0].grid(alpha= 0.3)

# 2. KDA: Wins vs Losses (Box plot)
box_data= [wins_df['kda_ratio'], losses_df['kda_ratio']]
bp= axes[0, 1].boxplot(box_data, labels= ['Wins', 'Losses'], patch_artist= True)
bp['boxes'][0].set_facecolor('#4CAF50')
bp['boxes'][1].set_facecolor('#F44336')
for box in bp['boxes']:
    box.set_alpha(0.7)
axes[0, 1].set_ylabel('KDA Ratio', fontsize= 12, fontweight= 'bold')
axes[0, 1].set_title('KDA: Wins vs Losses', fontsize= 13, fontweight= 'bold')
axes[0, 1].grid(axis= 'y', alpha= 0.3)

# 3. Kills distribution (Wins vs Losses)
axes[1, 0].hist([wins_df['kills'], losses_df['kills']], bins= 15, 
                label= ['Wins', 'Losses'], color= ['#4CAF50', '#F44336'], alpha= 0.7, edgecolor= 'black')
axes[1, 0].set_xlabel('Kills', fontsize= 12, fontweight= 'bold')
axes[1, 0].set_ylabel('Frequency', fontsize= 12, fontweight= 'bold')
axes[1, 0].set_title('Kills Distribution: Wins vs Losses', fontsize= 13, fontweight= 'bold')
axes[1, 0].legend()
axes[1, 0].grid(alpha= 0.3)

# 4. Deaths distribution (Wins vs Losses)
axes[1, 1].hist([wins_df['deaths'], losses_df['deaths']], bins= 12,
                label= ['Wins', 'Losses'], color= ['#4CAF50', '#F44336'], alpha= 0.7, edgecolor= 'black')
axes[1, 1].set_xlabel('Deaths', fontsize= 12, fontweight= 'bold')
axes[1, 1].set_ylabel('Frequency', fontsize= 12, fontweight= 'bold')
axes[1, 1].set_title('Deaths Distribution: Wins vs Losses', fontsize= 13, fontweight= 'bold')
axes[1, 1].legend()
axes[1, 1].grid(alpha= 0.3)

plt.tight_layout()
plt.show()


# ### Game Duration Analysis

# In[13]:


df_kata['duration_minutes']= df_kata['game_duration'] / 60

# Overall duration stats
print(f"\n OVERALL DURATION STATISTICS:")
print(f"   Average game: {df_kata['duration_minutes'].mean():.1f} minutes")
print(f"   Median game: {df_kata['duration_minutes'].median():.1f} minutes")
print(f"   Shortest game: {df_kata['duration_minutes'].min():.1f} minutes")
print(f"   Longest game: {df_kata['duration_minutes'].max():.1f} minutes")
print(f"   Std Dev: {df_kata['duration_minutes'].std():.1f} minutes")

# Duration in wins vs losses
print(f"\n DURATION: WINS vs LOSSES:")
print(f"   Wins - Average: {wins_df['game_duration'].mean() / 60:.1f} minutes")
print(f"   Wins - Median: {wins_df['game_duration'].median() / 60:.1f} minutes")
print(f"   Losses - Average: {losses_df['game_duration'].mean() / 60:.1f} minutes")
print(f"   Losses - Median: {losses_df['game_duration'].median() / 60:.1f} minutes")

duration_diff= (wins_df['game_duration'].mean() - losses_df['game_duration'].mean()) / 60
print(f"   Difference: {duration_diff:.1f} minutes")

if duration_diff < 0:
    print(f"You win FASTER games (by {abs(duration_diff):.1f} minutes)")
else:
    print(f"You win LONGER games (by {duration_diff:.1f} minutes)")

# Create duration categories
print(f"\n {'='*60}")
print("DURATION CATEGORIES:")
print("="*60)

def duration_category(minutes):
    if minutes < 20:
        return 'Very Short (<20min)'
    elif minutes < 25:
        return 'Short (20-25min)'
    elif minutes < 30:
        return 'Medium (25-30min)'
    elif minutes < 35:
        return 'Long (30-35min)'
    else:
        return 'Very Long (35min+)'

df_kata['duration_category']= df_kata['duration_minutes'].apply(duration_category)

# Distribution of games by duration
duration_dist= df_kata['duration_category'].value_counts().sort_index()
print(f"\n {duration_dist}")

# Win rate by duration category
print(f"\n {'='*60}")
print("WIN RATE BY GAME DURATION:")
print("="*60)

categories_order= ['Very Short (<20min)', 'Short (20-25min)', 'Medium (25-30min)', 
                    'Long (30-35min)', 'Very Long (35min+)']

for category in categories_order:
    if category in df_kata['duration_category'].values:
        cat_games= df_kata[df_kata['duration_category']== category]
        win_rate_cat= (cat_games['win'].sum() / len(cat_games) * 100)
        avg_duration= cat_games['duration_minutes'].mean()
        print(f"{category}: {win_rate_cat:.1f}% win rate ({len(cat_games)} games, avg: {avg_duration:.1f}min)")

# Visualizations
fig, axes= plt.subplots(2, 2, figsize= (15, 10))
fig.suptitle('Game Duration Analysis', fontsize= 16, fontweight= 'bold')

# 1. Duration distribution histogram
axes[0, 0].hist(df_kata['duration_minutes'], bins= 20, color= '#2196F3', alpha= 0.7, edgecolor= 'black')
axes[0, 0].axvline(df_kata['duration_minutes'].mean(), color= 'red', linestyle= '--', linewidth= 2,
                   label= f'Mean: {df_kata["duration_minutes"].mean():.1f}min')
axes[0, 0].axvline(df_kata['duration_minutes'].median(), color= 'green', linestyle= '--', linewidth= 2,
                   label= f'Median: {df_kata["duration_minutes"].median():.1f}min')
axes[0, 0].set_xlabel('Game Duration (minutes)', fontsize= 12, fontweight= 'bold')
axes[0, 0].set_ylabel('Frequency', fontsize= 12, fontweight= 'bold')
axes[0, 0].set_title('Overall Duration Distribution', fontsize= 13, fontweight= 'bold')
axes[0, 0].legend()
axes[0, 0].grid(alpha= 0.3)

# 2. Duration: Wins vs Losses (Box plot)
wins_duration= wins_df['game_duration'] / 60
losses_duration= losses_df['game_duration'] / 60
box_data= [wins_duration, losses_duration]
bp= axes[0, 1].boxplot(box_data, labels=['Wins', 'Losses'], patch_artist= True)
bp['boxes'][0].set_facecolor('#4CAF50')
bp['boxes'][1].set_facecolor('#F44336')
for box in bp['boxes']:
    box.set_alpha(0.7)
axes[0, 1].set_ylabel('Duration (minutes)', fontsize= 12, fontweight= 'bold')
axes[0, 1].set_title('Duration: Wins vs Losses', fontsize= 13, fontweight= 'bold')
axes[0, 1].grid(axis= 'y', alpha= 0.3)

# 3. Duration vs Outcome (Scatter plot)
wins_mins= wins_df['game_duration'] / 60
losses_mins= losses_df['game_duration'] / 60
axes[1, 0].scatter(wins_mins, [1]*len(wins_mins), color= '#4CAF50', alpha= 0.5, s= 50, label= 'Wins')
axes[1, 0].scatter(losses_mins, [0]*len(losses_mins), color= '#F44336', alpha= 0.5, s= 50, label= 'Losses')
axes[1, 0].set_xlabel('Game Duration (minutes)', fontsize= 12, fontweight= 'bold')
axes[1, 0].set_ylabel('Outcome', fontsize= 12, fontweight= 'bold')
axes[1, 0].set_yticks([0, 1])
axes[1, 0].set_yticklabels(['Loss', 'Win'])
axes[1, 0].set_title('Duration vs Outcome', fontsize= 13, fontweight= 'bold')
axes[1, 0].legend()
axes[1, 0].grid(alpha= 0.3)

# 4. Win rate by duration category
win_rates= []
categories= []
for category in categories_order:
    if category in df_kata['duration_category'].values:
        cat_games= df_kata[df_kata['duration_category']== category]
        win_rate_cat= (cat_games['win'].sum() / len(cat_games) * 100)
        win_rates.append(win_rate_cat)
        categories.append(category.split('(')[0].strip())

bars= axes[1, 1].bar(range(len(categories)), win_rates, color='#4CAF50', alpha= 0.7, edgecolor= 'black', linewidth= 2)
axes[1, 1].axhline(y= 50, color= 'red', linestyle= '--', linewidth= 2, label= '50% (Even)')
axes[1, 1].set_xticks(range(len(categories)))
axes[1, 1].set_xticklabels(categories, rotation= 45, ha= 'right')
axes[1, 1].set_ylabel('Win Rate (%)', fontsize= 12, fontweight= 'bold')
axes[1, 1].set_title('Win Rate by Duration Category', fontsize= 13, fontweight= 'bold')
axes[1, 1].set_ylim(0, 100)
axes[1, 1].legend()
axes[1, 1].grid(axis= 'y', alpha= 0.3)

# Add value labels on bars
for i, (bar, rate) in enumerate(zip(bars, win_rates)):
    height= bar.get_height()
    axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{rate:.1f}%',
                    ha='center', va= 'bottom', fontsize= 10, fontweight= 'bold')

plt.tight_layout()
plt.show()

# Performance metrics by duration
print(f"\n {'='*60}")
print("PERFORMANCE BY DURATION CATEGORY:")
print("="*60)

performance_stats= ['kills', 'deaths', 'kda_ratio', 'damage_per_min', 'cs_per_min']

for category in categories_order:
    if category in df_kata['duration_category'].values:
        cat_games= df_kata[df_kata['duration_category']== category]
        print(f"\n {category}:")
        print(f"   Games: {len(cat_games)}")
        print(f"   Win Rate: {(cat_games['win'].sum() / len(cat_games) * 100):.1f}%")
        print(f"   Avg Kills: {cat_games['kills'].mean():.1f}")
        print(f"   Avg Deaths: {cat_games['deaths'].mean():.1f}")
        print(f"   Avg KDA: {cat_games['kda_ratio'].mean():.1f}")
        print(f"   Damage/min: {cat_games['damage_per_min'].mean():.0f}")


# ### Team Objectives Analysis

# In[25]:


# Overall objectives stats
print(f"\n OVERALL OBJECTIVES STATISTICS:")
print(f"   Average Dragons: {df_kata['team_dragons'].mean():.2f}")
print(f"   Average Barons: {df_kata['team_barons'].mean():.2f}")
print(f"   Average Towers: {df_kata['team_towers'].mean():.2f}")
print(f"   First Blood Rate: {(df_kata['first_blood'].sum() / len(df_kata) * 100):.1f}%")

# Objectives in wins vs losses
print(f"\n OBJECTIVES: WINS vs LOSSES:")

objectives= ['team_dragons', 'team_barons', 'team_towers', 'first_blood']
obj_names= ['Dragons', 'Barons', 'Towers', 'First Blood']

for obj, name in zip(objectives, obj_names):
    wins_avg= wins_df[obj].mean()
    losses_avg= losses_df[obj].mean()
    diff= wins_avg - losses_avg
    pct_diff= (diff / losses_avg * 100) if losses_avg > 0 else 0
    
    print(f"\n {name.upper()}:")
    print(f"    Wins: {wins_avg:.2f}")
    print(f"    Losses: {losses_avg:.2f}")
    print(f"    Difference: {diff:.2f} ({pct_diff:.1f}%)")

# Dragon categories
print(f"\n {'='*60}")
print("DRAGON CONTROL ANALYSIS:")
print("="*60)

def dragon_category(dragons):
    if dragons== 0:
        return 'No Dragons (0)'
    elif dragons== 1:
        return 'Low Dragons (1)'
    elif dragons== 2:
        return 'Medium Dragons (2)'
    elif dragons== 3:
        return 'High Dragons (3)'
    else:
        return 'Dragon Soul (4+)'

df_kata['dragon_category']= df_kata['team_dragons'].apply(dragon_category)

# Win rate by dragon count
dragon_order= ['No Dragons (0)', 'Low Dragons (1)', 'Medium Dragons (2)', 
                'High Dragons (3)', 'Dragon Soul (4+)']

print(f"\n WIN RATE BY DRAGON COUNT:")
for category in dragon_order:
    if category in df_kata['dragon_category'].values:
        cat_games= df_kata[df_kata['dragon_category']== category]
        win_rate= (cat_games['win'].sum() / len(cat_games) * 100)
        dragon_count= cat_games['team_dragons'].mean()
        print(f"{category}: {win_rate:.1f}% win rate ({len(cat_games)} games)")

# Baron impact
print(f"\n {'='*60}")
print("BARON IMPACT ANALYSIS:")
print("="*60)

baron_stats= df_kata.groupby('team_barons').agg({
    'win': ['count', 'sum', 'mean']
}).round(3)

print(f"\nWIN RATE BY BARON COUNT:")
for baron_count in sorted(df_kata['team_barons'].unique()):
    baron_games= df_kata[df_kata['team_barons']== baron_count]
    win_rate= (baron_games['win'].sum() / len(baron_games) * 100)
    print(f"{baron_count} Barons: {win_rate:.1f}% win rate ({len(baron_games)} games)")

# Tower categories
print(f"\n {'='*60}")
print("TOWER CONTROL ANALYSIS:")
print("="*60)

def tower_category(towers):
    if towers <= 2:
        return 'Low Towers (0-2)'
    elif towers <= 5:
        return 'Medium Towers (3-5)'
    elif towers <= 8:
        return 'High Towers (6-8)'
    else:
        return 'Full Push (9+)'

df_kata['tower_category']= df_kata['team_towers'].apply(tower_category)

tower_order= ['Low Towers (0-2)', 'Medium Towers (3-5)', 
               'High Towers (6-8)', 'Full Push (9+)']

print(f"\n WIN RATE BY TOWER COUNT:")
for category in tower_order:
    if category in df_kata['tower_category'].values:
        cat_games= df_kata[df_kata['tower_category']== category]
        win_rate= (cat_games['win'].sum() / len(cat_games) * 100)
        avg_towers= cat_games['team_towers'].mean()
        print(f"{category}: {win_rate:.1f}% win rate ({len(cat_games)} games, avg: {avg_towers:.1f})")

# First Blood impact
print(f"\n {'='*60}")
print("FIRST BLOOD IMPACT:")
print("="*60)

fb_yes= df_kata[df_kata['first_blood']== 1]
fb_no= df_kata[df_kata['first_blood']== 0]

fb_yes_wr= (fb_yes['win'].sum() / len(fb_yes) * 100)
fb_no_wr= (fb_no['win'].sum() / len(fb_no) * 100)

print(f"\n Team Got First Blood: {fb_yes_wr:.1f}% win rate ({len(fb_yes)} games)")
print(f"Team Lost First Blood: {fb_no_wr:.1f}% win rate ({len(fb_no)} games)")
print(f"Difference: {fb_yes_wr - fb_no_wr:.1f}%")

# Visualizations
fig, axes= plt.subplots(2, 3, figsize= (18, 10))
fig.suptitle('Team Objectives Analysis', fontsize= 16, fontweight= 'bold')

# 1. Dragons: Wins vs Losses
axes[0, 0].hist([wins_df['team_dragons'], losses_df['team_dragons']], bins= 7,
                label= ['Wins', 'Losses'], color= ['#4CAF50', '#F44336'], alpha= 0.7, edgecolor= 'black')
axes[0, 0].set_xlabel('Dragons', fontsize= 12, fontweight= 'bold')
axes[0, 0].set_ylabel('Frequency', fontsize= 12, fontweight= 'bold')
axes[0, 0].set_title('Dragons Distribution: Wins vs Losses', fontsize= 13, fontweight= 'bold')
axes[0, 0].legend()
axes[0, 0].grid(alpha= 0.3)

# 2. Win Rate by Dragon Count
dragon_wr= []
dragon_labels= []
for category in dragon_order:
    if category in df_kata['dragon_category'].values:
        cat_games= df_kata[df_kata['dragon_category']== category]
        wr= (cat_games['win'].sum() / len(cat_games) * 100)
        dragon_wr.append(wr)
        dragon_labels.append(category.split('(')[0].strip())

bars= axes[0, 1].bar(range(len(dragon_labels)), dragon_wr, color= '#4CAF50', alpha= 0.7, edgecolor= 'black', linewidth= 2)
axes[0, 1].axhline(y= 50, color= 'red', linestyle= '--', linewidth= 2, label= '50%')
axes[0, 1].set_xticks(range(len(dragon_labels)))
axes[0, 1].set_xticklabels(dragon_labels, rotation= 45, ha= 'right')
axes[0, 1].set_ylabel('Win Rate (%)', fontsize= 12, fontweight= 'bold')
axes[0, 1].set_title('Win Rate by Dragon Count', fontsize= 13, fontweight= 'bold')
axes[0, 1].set_ylim(0, 100)
axes[0, 1].legend()
axes[0, 1].grid(axis= 'y', alpha= 0.3)

for i, (bar, wr) in enumerate(zip(bars, dragon_wr)):
    height= bar.get_height()
    axes[0, 1].text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{wr:.1f}%', ha= 'center', va= 'bottom', fontsize= 10, fontweight= 'bold')

# 3. Baron Impact
baron_wr_list= []
baron_counts= sorted(df_kata['team_barons'].unique())
for baron_count in baron_counts:
    baron_games= df_kata[df_kata['team_barons']== baron_count]
    wr= (baron_games['win'].sum() / len(baron_games) * 100)
    baron_wr_list.append(wr)

bars= axes[0, 2].bar(baron_counts, baron_wr_list, color='#9C27B0', alpha=0.7, edgecolor='black', linewidth=2)
axes[0, 2].axhline(y= 50, color= 'red', linestyle= '--', linewidth= 2, label= '50%')
axes[0, 2].set_xlabel('Baron Count', fontsize= 12, fontweight= 'bold')
axes[0, 2].set_ylabel('Win Rate (%)', fontsize= 12, fontweight= 'bold')
axes[0, 2].set_title('Win Rate by Baron Count', fontsize= 13, fontweight= 'bold')
axes[0, 2].set_ylim(0, 100)
axes[0, 2].legend()
axes[0, 2].grid(axis= 'y', alpha= 0.3)

for bar, wr in zip(bars, baron_wr_list):
    height= bar.get_height()
    axes[0, 2].text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{wr:.1f}%', ha= 'center', va='bottom', fontsize= 10, fontweight= 'bold')

# 4. Towers: Wins vs Losses
axes[1, 0].hist([wins_df['team_towers'], losses_df['team_towers']], bins= 12,
                label= ['Wins', 'Losses'], color= ['#4CAF50', '#F44336'], alpha= 0.7, edgecolor= 'black')
axes[1, 0].set_xlabel('Towers', fontsize= 12, fontweight= 'bold')
axes[1, 0].set_ylabel('Frequency', fontsize= 12, fontweight= 'bold')
axes[1, 0].set_title('Towers Distribution: Wins vs Losses', fontsize= 13, fontweight= 'bold')
axes[1, 0].legend()
axes[1, 0].grid(alpha= 0.3)

# 5. Win Rate by Tower Count
tower_wr= []
tower_labels= []
for category in tower_order:
    if category in df_kata['tower_category'].values:
        cat_games= df_kata[df_kata['tower_category']== category]
        wr = (cat_games['win'].sum() / len(cat_games) * 100)
        tower_wr.append(wr)
        tower_labels.append(category.split('(')[0].strip())

bars= axes[1, 1].bar(range(len(tower_labels)), tower_wr, color = '#FF9800', alpha= 0.7, edgecolor= 'black', linewidth= 2)
axes[1, 1].axhline(y= 50, color= 'red', linestyle= '--', linewidth= 2, label= '50%')
axes[1, 1].set_xticks(range(len(tower_labels)))
axes[1, 1].set_xticklabels(tower_labels, rotation= 45, ha= 'right')
axes[1, 1].set_ylabel('Win Rate (%)', fontsize= 12, fontweight= 'bold')
axes[1, 1].set_title('Win Rate by Tower Count', fontsize= 13, fontweight= 'bold')
axes[1, 1].set_ylim(0, 100)
axes[1, 1].legend()
axes[1, 1].grid(axis= 'y', alpha= 0.3)

for i, (bar, wr) in enumerate(zip(bars, tower_wr)):
    height= bar.get_height()
    axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{wr:.1f}%', ha= 'center', va= 'bottom', fontsize= 10, fontweight= 'bold')

# 6. First Blood Impact
fb_data= [fb_yes_wr, fb_no_wr]
fb_labels= ['Got FB', 'Lost FB']
bars= axes[1, 2].bar(fb_labels, fb_data, color= ['#4CAF50', '#F44336'], alpha= 0.7, edgecolor= 'black', linewidth= 2)
axes[1, 2].axhline(y= 50, color= 'red', linestyle= '--', linewidth= 2, label= '50%')
axes[1, 2].set_ylabel('Win Rate (%)', fontsize= 12, fontweight= 'bold')
axes[1, 2].set_title('First Blood Impact', fontsize= 13, fontweight= 'bold')
axes[1, 2].set_ylim(0, 100)
axes[1, 2].legend()
axes[1, 2].grid(axis= 'y', alpha= 0.3)

for bar, wr in zip(bars, fb_data):
    height= bar.get_height()
    axes[1, 2].text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{wr:.1f}%', ha= 'center', va= 'bottom', fontsize= 12, fontweight= 'bold')

plt.tight_layout()
plt.show()

# Combined objectives analysis
print(f"\n {'='*60}")
print("COMBINED OBJECTIVES SCORE:")
print("="*60)

# Recreate wins_df and losses_df AFTER adding objective_score
wins_df= df_kata[df_kata['win'] == 1]
losses_df= df_kata[df_kata['win'] == 0]

# Create objective score (weighted)
df_kata['objective_score']= (df_kata['team_dragons'] * 2 + 
                               df_kata['team_barons'] * 3 + 
                               df_kata['team_towers'] * 1)

print(f"\n Objective Score = (Dragons × 2) + (Barons × 3) + (Towers × 1)")
print(f"\n Average Objective Score:")
print(f"   Overall: {df_kata['objective_score'].mean():.1f}")
print(f"   Wins: {wins_df['objective_score'].mean():.1f}")
print(f"   Losses: {losses_df['objective_score'].mean():.1f}")
print(f"   Difference: {wins_df['objective_score'].mean() - losses_df['objective_score'].mean():.1f}")


# ### Correlation Heatmap 

# In[26]:


# Select numeric features for correlation analysis
numeric_features= ['win', 'game_duration', 'kills', 'deaths', 'assists', 
                   'cs', 'gold_earned', 'damage_to_champions', 'damage_taken', 
                   'level', 'team_dragons', 'team_barons', 'team_towers', 
                   'first_blood', 'kda_ratio', 'cs_per_min', 'gold_per_min', 
                   'damage_per_min', 'kill_participation', 'kill_share', 'death_share']

correlation_matrix= df_kata[numeric_features].corr()

# Get correlation with 'win' and sort
correlation_with_win= correlation_matrix['win'].sort_values(ascending=False)

print(f"\n CORRELATION WITH WINNING (sorted):")
print("="*60)
print(correlation_with_win)

print(f"\n {'='*60}")
print("TOP 10 POSITIVE CORRELATIONS WITH WINNING:")
print("="*60)

# Exclude 'win' itself
top_10_positive= correlation_with_win[1:11]
for i, (feature, corr) in enumerate(top_10_positive.items(), 1):
    print(f"{i:2d}. {feature:25s}: {corr:+.3f}")

print(f"\n {'='*60}")
print("TOP 5 NEGATIVE CORRELATIONS WITH WINNING:")
print("="*60)
bottom_5_negative= correlation_with_win[-5:]
for i, (feature, corr) in enumerate(bottom_5_negative.items(), 1):
    print(f"{i:2d}. {feature:25s}: {corr:+.3f}")

# Create comprehensive heatmap
fig, axes= plt.subplots(1, 2, figsize= (20, 10))
fig.suptitle('Correlation Analysis', fontsize= 16, fontweight= 'bold')

# 1. Full correlation heatmap
im1= axes[0].imshow(correlation_matrix, cmap= 'coolwarm', aspect= 'auto', vmin= -1, vmax= 1)
axes[0].set_xticks(range(len(numeric_features)))
axes[0].set_yticks(range(len(numeric_features)))
axes[0].set_xticklabels(numeric_features, rotation= 90, ha= 'right', fontsize= 9)
axes[0].set_yticklabels(numeric_features, fontsize= 9)
axes[0].set_title('Full Correlation Matrix', fontsize= 14, fontweight= 'bold')

cbar1= plt.colorbar(im1, ax= axes[0])
cbar1.set_label('Correlation Coefficient', fontsize= 11, fontweight= 'bold')

# Add correlation values (only for high correlations to avoid clutter)
for i in range(len(numeric_features)):
    for j in range(len(numeric_features)):
        corr_val= correlation_matrix.iloc[i, j]
        if abs(corr_val) > 0.5 and i != j: 
            text_color= 'white' if abs(corr_val) > 0.7 else 'black'
            axes[0].text(j, i, f'{corr_val:.2f}', 
                        ha= 'center', va= 'center', 
                        color= text_color, fontsize= 7, fontweight= 'bold')

# 2. Correlation with Win (bar chart)
# Exclude 'win' itself
win_corr_sorted= correlation_with_win[1:].sort_values()  
colors= ['#F44336' if x < 0 else '#4CAF50' for x in win_corr_sorted.values]

axes[1].barh(range(len(win_corr_sorted)), win_corr_sorted.values, color= colors, alpha= 0.7, edgecolor= 'black')
axes[1].set_yticks(range(len(win_corr_sorted)))
axes[1].set_yticklabels(win_corr_sorted.index, fontsize= 10)
axes[1].axvline(x= 0, color= 'black', linestyle= '-', linewidth= 1)
axes[1].set_xlabel('Correlation with Win', fontsize= 12, fontweight= 'bold')
axes[1].set_title('Feature Correlation with Winning', fontsize= 14, fontweight= 'bold')
axes[1].grid(axis= 'x', alpha= 0.3)

for i, (feature, corr) in enumerate(win_corr_sorted.items()):
    x_pos= corr + (0.02 if corr > 0 else -0.02)
    ha= 'left' if corr > 0 else 'right'
    axes[1].text(x_pos, i, f'{corr:.3f}', 
                ha= ha, va= 'center', fontsize= 9, fontweight= 'bold')

plt.tight_layout()
plt.show()

# Additional analysis: Feature groups
print(f"\n{'='*60}")
print("CORRELATION BY FEATURE GROUPS:")
print("="*60)

# Group 1: Your Performance
performance_features= ['kills', 'deaths', 'assists', 'kda_ratio', 
                       'kill_participation', 'kill_share', 'death_share']
print(f"\n YOUR PERFORMANCE:")
for feat in performance_features:
    if feat in correlation_with_win.index:
        print(f"   {feat:25s}: {correlation_with_win[feat]:+.3f}")

# Group 2: Gold
economy_features= ['cs', 'cs_per_min', 'gold_earned', 'gold_per_min']
print(f"\n GOLD:")
for feat in economy_features:
    if feat in correlation_with_win.index:
        print(f"   {feat:25s}: {correlation_with_win[feat]:+.3f}")

# Group 3: Combat
combat_features= ['damage_to_champions', 'damage_per_min', 'damage_taken', 'level']
print(f"\n COMBAT:")
for feat in combat_features:
    if feat in correlation_with_win.index:
        print(f"   {feat:25s}: {correlation_with_win[feat]:+.3f}")

# Group 4: Team Objectives
objective_features= ['team_dragons', 'team_barons', 'team_towers', 'first_blood']
print(f"\n TEAM OBJECTIVES:")
for feat in objective_features:
    if feat in correlation_with_win.index:
        print(f"   {feat:25s}: {correlation_with_win[feat]:+.3f}")

# Group 5: Game Context
context_features= ['game_duration']
print(f"\n GAME CONTEXT:")
for feat in context_features:
    if feat in correlation_with_win.index:
        print(f"   {feat:25s}: {correlation_with_win[feat]:+.3f}")

# Multicollinearity check
print(f"\n{'='*60}")
print("HIGHLY CORRELATED FEATURES (Multicollinearity):")
print("="*60)
print("Features with correlation > 0.8 (excluding 'win'):")

high_corr_pairs= []
for i in range(len(numeric_features)):
    for j in range(i+1, len(numeric_features)):
        feat1= numeric_features[i]
        feat2= numeric_features[j]
        if feat1 != 'win' and feat2 != 'win':
            corr_val= correlation_matrix.loc[feat1, feat2]
            if abs(corr_val) > 0.8:
                high_corr_pairs.append((feat1, feat2, corr_val))

if high_corr_pairs:
    for feat1, feat2, corr in sorted(high_corr_pairs, key= lambda x: abs(x[2]), reverse= True):
        print(f"   {feat1:25s} <-> {feat2:25s}: {corr:+.3f}")
else:
    print("No highly correlated feature pairs found!")

# Summary
print(f"\n {'='*60}")
print("KEY FINDINGS SUMMARY:")
print("="*60)

strongest_positive= correlation_with_win[1:4]
strongest_negative= correlation_with_win[-3:]

print(f"\n STRONGEST POSITIVE PREDICTORS:")
for i, (feat, corr) in enumerate(strongest_positive.items(), 1):
    print(f"{i}. {feat}: {corr:+.3f}")

print(f"\n STRONGEST NEGATIVE PREDICTORS:")
for i, (feat, corr) in enumerate(strongest_negative.items(), 1):
    print(f"{i}. {feat}: {corr:+.3f}")

print(f"\n INSIGHTS:")
print(f"- Top predictor: {correlation_with_win.index[1]} ({correlation_with_win.iloc[1]:+.3f})")
print(f"- Weakest predictor: {correlation_with_win.index[-1]} ({correlation_with_win.iloc[-1]:+.3f})")
print(f"- Range: {correlation_with_win.iloc[-1]:.3f} to {correlation_with_win.iloc[1]:+.3f}")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




