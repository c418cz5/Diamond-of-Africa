mport pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
plt.rcParams['font.sans-serif'] = ['SimHei']

netflix = pd.read_csv('netflix_titles.csv')
amazon = pd.read_csv('amazon_prime_titles.csv')
disney = pd.read_csv('disney_plus_titles.csv')
hulu = pd.read_csv('hulu_titles.csv')

def clean_data(df, platform):
    df['platform'] = platform  # 添加平台标识
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')  # 统一日期格式
    df['release_year'] = df['release_year'].fillna(0).astype(int)  # 处理年份空值
    return df
netflix_clean = clean_data(netflix, 'Netflix')
amazon_clean = clean_data(amazon, 'Amazon Prime')
disney_clean = clean_data(disney, 'Disney+')
hulu_clean = clean_data(hulu, 'Hulu')

def count_content_type(df):
    total = len(df)
    movie = len(df[df['type'] == 'Movie'])
    tv_show = len(df[df['type'] == 'TV Show'])
    return total, movie, tv_show

platform_stats = {
    'Netflix': count_content_type(netflix_clean),
    'Amazon Prime': count_content_type(amazon_clean),
    'Disney+': count_content_type(disney_clean),
    'Hulu': count_content_type(hulu_clean)
}
def get_top_genres(df):
    all_genres = []
    for genre_str in df['listed_in'].dropna():
        genres = [g.strip() for g in genre_str.split(',')]
        all_genres.extend(genres)
    return Counter(all_genres).most_common(5)

netflix_top5 = get_top_genres(netflix_clean)


import os
if not os.path.exists('chart_'):
    os.makedirs('chart_')
plt.figure(figsize=(12, 6))
platforms = list(platform_stats.keys())
movie_counts = [platform_stats[p][1] for p in platforms]
tv_counts = [platform_stats[p][2] for p in platforms]

plt.bar(platforms, movie_counts, label='Movies', color='#E50914')
plt.bar(platforms, tv_counts, bottom=movie_counts, label='TV Shows', color='#1428A0')
plt.title('Content Volume by Streaming Platform (Movie vs TV Show)')
plt.ylabel('Number of Contents')
plt.xlabel('Platform')
plt.legend()
plt.savefig('chart_/content_type_count.png', dpi=300, bbox_inches='tight')  # Save high-res chart
plt.close()   

plt.figure(figsize=(8, 8))
genres = [g[0] for g in netflix_top5]
counts = [g[1] for g in netflix_top5]
plt.pie(counts, labels=genres, autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)
plt.title('Netflix: Top 5 Popular Genres')
plt.savefig('chart_/netflix_top5_genres.png', dpi=300, bbox_inches='tight')
plt.close()

all_clean_data = pd.concat([netflix_clean, amazon_clean, disney_clean, hulu_clean], ignore_index=True)
yearly_trend = all_clean_data[all_clean_data['release_year'] >= 2010].groupby(['release_year', 'platform']).size().unstack(fill_value=0)

plt.figure(figsize=(14, 7))
for platform in yearly_trend.columns:
    plt.plot(yearly_trend.index, yearly_trend[platform], marker='o', label=platform)
plt.title('Yearly Content Release Trend (2010-2023) by Platform')
plt.ylabel('Number of New Contents')
plt.xlabel('Release Year')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('chart_/yearly_content_trend.png', dpi=300, bbox_inches='tight')
plt.close()

print("=== Content Volume Statistics by Platform ===")
for p, (total, movie, tv) in platform_stats.items():
    movie_ratio = round(movie/total, 2)
    tv_ratio = round(tv/total, 2)
    print(f"{p}: Total {total} contents | Movies: {movie} ({movie_ratio}) | TV Shows: {tv} ({tv_ratio})")

print("\n=== Netflix: Top 5 Popular Genres ===")
for genre, count in netflix_top5:
    print(f"{genre}: {count} occurrences")

print("\n=== Analysis Complete! Charts saved to 'chart_' folder. ===")
