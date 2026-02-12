"""
MotoGP 2024 - Data Visualization

- Wins by rider
- Pole positions
- Win distribution
- Performance comparison
- Championship battle progression

"""
# ### Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.cloud import storage
from io import StringIO
import os

# ### Configuration
PROJECT_ID= 'motogp-racing-analytics'
BUCKET_NAME= 'motogp-racing-data-2024'
FILE_NAME= 'motogp_2024_results.csv'

# ### Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize']= (12, 6)
plt.rcParams['font.size']= 10

def load_data():
    """Load data from Cloud Storage"""
    
    storage_client= storage.Client(project= PROJECT_ID)
    bucket= storage_client.bucket(BUCKET_NAME)
    blob= bucket.blob(FILE_NAME)
    csv_data= blob.download_as_text()
    df= pd.read_csv(StringIO(csv_data))
    
    print(f"Data loaded {len(df)} rows, {len(df.columns)} columns")
    return df

def create_wins_chart(df):
    """Chart 1: Wins by Rider"""
    
    wins= df['Winning rider'].value_counts().head(10)
    
    plt.figure(figsize= (12, 6))
    bars= plt.bar(range(len(wins)), wins.values, color='#e10600', edgecolor= 'black', linewidth= 1.2)
    
    plt.xlabel('Rider', fontsize= 12, fontweight= 'bold')
    plt.ylabel('Number of Wins', fontsize= 12, fontweight= 'bold')
    plt.title('MotoGP 2024 - Race Wins by Rider', fontsize=16, fontweight= 'bold', pad= 20)
    plt.xticks(range(len(wins)), wins.index, rotation= 45, ha= 'right')
    plt.grid(axis= 'y', alpha= 0.3)
    
    for i, (bar, value) in enumerate(zip(bars, wins.values)):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, 
                 str(value), ha= 'center', va= 'bottom', fontweight= 'bold', fontsize= 11)
    
    plt.tight_layout()
    plt.savefig('005_visualizations/viz_01_wins_by_rider.png', dpi= 300, bbox_inches= 'tight')
    plt.close()

def create_poles_chart(df):
    """Chart 2: Pole Positions"""
        
    poles= df['Pole position'].value_counts().head(10)
    
    plt.figure(figsize= (12, 7))
    bars= plt.barh(range(len(poles)), poles.values, color= '#ffd700', 
                    edgecolor= 'black', linewidth= 1.2)
    
    plt.xlabel('Number of Pole Positions', fontsize= 12, fontweight= 'bold')
    plt.ylabel('Rider', fontsize= 12, fontweight= 'bold')
    plt.title('MotoGP 2024 - Pole Positions by Rider', fontsize= 16, fontweight= 'bold', pad= 20)
    plt.yticks(range(len(poles)), poles.index)
    plt.grid(axis= 'x', alpha= 0.3)
    
    for i, (bar, value) in enumerate(zip(bars, poles.values)):
        plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                 str(value), ha= 'left', va= 'center', fontweight= 'bold', fontsize= 11)
    
    plt.tight_layout()
    plt.savefig('005_visualizations/viz_02_pole_positions.png', dpi= 300, bbox_inches= 'tight')
    plt.close()

def create_pie_chart(df):
    """Chart 3: Win Distribution."""
        
    wins_top5= df['Winning rider'].value_counts().head(5)
    
    plt.figure(figsize= (10, 8))
    colors= ['#e10600', '#ff4444', '#ff7777', '#ffaaaa', '#ffdddd']
    explode= (0.1, 0.05, 0.05, 0, 0)
    
    wedges, texts, autotexts = plt.pie(wins_top5.values, 
                                       labels= wins_top5.index,
                                       autopct= '%1.1f%%',
                                       startangle= 90,
                                       colors= colors,
                                       explode= explode,
                                       shadow= True,
                                       textprops= {'fontsize': 11, 'fontweight': 'bold'})
    
    plt.title('MotoGP 2024 - Win Distribution (Top 5 Riders)', fontsize= 16, fontweight= 'bold', pad= 20)
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
    
    plt.tight_layout()
    plt.savefig('005_visualizations/viz_03_win_distribution.png', dpi= 300, bbox_inches= 'tight')
    plt.close()

def create_comparison_chart(df):
    """Chart 4: Performance Comparison."""
        
    top_riders= df['Winning rider'].value_counts().head(5).index
    
    data_comparison= []
    for rider in top_riders:
        wins_count= len(df[df['Winning rider'] == rider])
        poles_count= len(df[df['Pole position'] == rider])
        fastest_count= len(df[df['Fastest lap'] == rider])
        data_comparison.append({'Rider': rider,
                                'Wins': wins_count,
                                'Poles': poles_count,
                                'Fastest Laps': fastest_count
                                })
    
    df_comparison= pd.DataFrame(data_comparison)
    
    x= range(len(df_comparison))
    width= 0.25
    
    fig, ax= plt.subplots(figsize= (14, 7))
    
    bars1= ax.bar([i - width for i in x], df_comparison['Wins'], width, label= 'Wins', color= '#e10600', edgecolor= 'black', linewidth= 1)
    bars2 = ax.bar([i for i in x], df_comparison['Poles'], width, label= 'Pole Positions', color= '#ffd700', edgecolor= 'black', linewidth= 1)
    bars3 = ax.bar([i + width for i in x], df_comparison['Fastest Laps'], width, label= 'Fastest Laps', color= '#4169e1', edgecolor= 'black', linewidth= 1)
    
    ax.set_xlabel('Rider', fontsize= 12, fontweight= 'bold')
    ax.set_ylabel('Count', fontsize= 12, fontweight= 'bold')
    ax.set_title('MotoGP 2024 - Performance Comparison (Top 5 Riders)', fontsize= 16, fontweight= 'bold', pad= 20)
    ax.set_xticks(x)
    ax.set_xticklabels(df_comparison['Rider'], rotation= 45, ha= 'right')
    ax.legend(fontsize= 11)
    ax.grid(axis= 'y', alpha= 0.3)
    
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height= bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.2, f'{int(height)}', ha= 'center', va= 'bottom', fontweight= 'bold', fontsize= 9)
    
    plt.tight_layout()
    plt.savefig('005_visualizations/viz_04_performance_comparison.png', dpi= 300, bbox_inches= 'tight')
    plt.close()

def create_championship_chart(df):
    """Chart 5: Championship Battle."""
    
    top_3_riders= df['Winning rider'].value_counts().head(3).index.tolist()
    
    cumulative_wins= {rider: [] for rider in top_3_riders}
    
    for race_num in range(1, len(df) + 1):
        races_so_far= df.head(race_num)
        for rider in top_3_riders:
            wins_count= len(races_so_far[races_so_far['Winning rider']== rider])
            cumulative_wins[rider].append(wins_count)
    
    plt.figure(figsize= (14, 7))
    colors_line= ['#e10600', '#0066cc', '#ff8800']
    
    for rider, color in zip(top_3_riders, colors_line):
        plt.plot(range(1, len(df) + 1), cumulative_wins[rider], marker= 'o', linewidth= 3, markersize= 8, label= rider, color= color, markeredgecolor= 'black', markeredgewidth= 1)
    
    plt.xlabel('Race Number', fontsize= 12, fontweight= 'bold')
    plt.ylabel('Cumulative Wins', fontsize= 12, fontweight= 'bold')
    plt.title('MotoGP 2024 - Championship Battle (Top 3 Riders)', fontsize= 16, fontweight= 'bold', pad= 20)
    plt.legend(fontsize= 12, loc= 'upper left', frameon= True, shadow= True)
    plt.grid(True, alpha= 0.3)
    plt.xticks(range(1, len(df) + 1, 2))
    
    plt.tight_layout()
    plt.savefig('005_visualizations/viz_05_championship_battle.png', dpi= 300, bbox_inches= 'tight')
    plt.close()

def main():
    """Main function to create all visualizations"""
    print("=" * 60)
    print("MotoGP 2024 - Data Visualization")
    print("=" * 60)
    print()
    
    df= load_data()
    print()
    
    create_wins_chart(df)
    create_poles_chart(df)
    create_pie_chart(df)
    create_comparison_chart(df)
    create_championship_chart(df)
    
    print("Key Insights:")
    print(f"Champion: {df['Winning rider'][0]} with {df['Winning rider'].value_counts().iloc[0]} wins!")
    print(f"Total races: {len(df)}")
    print(f"Different winners: {df['Winning rider'].nunique()}")
    
if __name__ == "__main__":
    main()