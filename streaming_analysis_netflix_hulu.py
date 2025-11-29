# This code is manually written, no AI assistance used
import pandas as pd
import matplotlib.pyplot as plt
import os

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

netflix_path = "C:\\Users\\Admin\\OneDrive - Navitas Limited\\DDWT\\netflix_titles.csv"
hulu_path ="C:\\Users\\Admin\\OneDrive - Navitas Limited\\DDWT\\hulu_titles.csv"

# LET ME CHECK  if files exits

if not os.path.exists(netflix_path) or not os.path.exists(hulu_path):
    print("Error: CSV files not found! Please check the paths.")
else:
    netflix = pd.read_csv(netflix_path)
    hulu = pd.read_csv(hulu_path)


# clean Data

def clean_data(df, platform):
        df['platform'] = platform
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
        df['release_year'] = df['release_year'].fillna(0).astype(int)
        return df

netflix_clean = clean_data(netflix, 'Netflix')
hulu_clean = clean_data(hulu, 'Hulu')
combined_data = pd.concat([netflix_clean, hulu_clean], ignore_index=True)


#  content the type distriburtion (movie tv show )

content_type = combined_data.groupby(['platform', 'type']).size().unstack(fill_value=0)
print("=== Content Type Distribution (Netflix vs Hulu) ===")
print(content_type)

# for netflix

def get_top_genres(df):
        all_genres = []
        for genre_str in df['listed_in'].dropna():
            genres = [g.strip() for g in genre_str.split(',')]
            all_genres.extend(genres)
        from collections import Counter
        return Counter(all_genres).most_common(5)

netflix_top5 = get_top_genres(netflix_clean)
print("\n=== Netflix Top 5 Genres ===")
for genre, count in netflix_top5:
    print(f"{genre}: {count} occurrences")

if not os.path.exists('chart_'):
        os.makedirs('chart_')


content_type.plot(kind='bar', figsize=(10, 6), color=['#E50914', '#1428A0'])
plt.title('Content Type: Netflix vs Hulu (Movie/TV Show)')
plt.ylabel('Number of Contents')
plt.xlabel('Platform')
plt.savefig('chart_/content_type_comparison.png', dpi=300, bbox_inches='tight')
plt.close()


genres = [g[0] for g in netflix_top5]
counts = [g[1] for g in netflix_top5]
plt.pie(counts, labels=genres, autopct='%1.1f%%', startangle=90)
plt.title('Netflix: Top 5 Popular Genres')
plt.savefig('chart_/netflix_top5_genres.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n=== Analysis Complete! Charts saved to 'chart_' folder. ===")