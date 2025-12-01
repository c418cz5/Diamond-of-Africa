mport pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
plt.rcParams['font.sans-serif'] = ['SimHei']
#显示中文
netflix = pd.read_csv('netflix_titles.csv')
amazon = pd.read_csv('amazon_prime_titles.csv')
disney = pd.read_csv('disney_plus_titles.csv')
hulu = pd.read_csv('hulu_titles.csv')
#导入库 加载  放在同一个文件夹
def clean_data(df, platform):
    df['platform'] = platform  #标签 区分netflix 和amazon
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')  # 统一日期格式
    df['release_year'] = df['release_year'].fillna(0).astype(int)  # 处理年份空值
    return df
    #调用函数清洗4个平台
netflix_clean = clean_data(netflix, 'Netflix')
amazon_clean = clean_data(amazon, 'Amazon Prime')
disney_clean = clean_data(disney, 'Disney+')
hulu_clean = clean_data(hulu, 'Hulu')
#errors='coerce'作用是 如果原始数据中date_added有非日期格式
def count_content_type(df):
    total = len(df)
    movie = len(df[df['type'] == 'Movie'])
    tv_show = len(df[df['type'] == 'TV Show'])
    return total, movie, tv_show
#统计4个平台的类型数据，存入字典
platform_stats = {
    'Netflix': count_content_type(netflix_clean),
    'Amazon Prime': count_content_type(amazon_clean),
    'Disney+': count_content_type(disney_clean),
    'Hulu': count_content_type(hulu_clean)
}
def get_top_genres(df):
    all_genres = [] #存储所有拆分的类型
    for genre_str in df['listed_in'].dropna():#遍历非空的类型字符
        genres = [g.strip() for g in genre_str.split(',')] #拆分加去空格
        all_genres.extend(genres) #把拆分后的类型加入总列表
    return Counter(all_genres).most_common(5) #统计top 5类型

netflix_top5 = get_top_genres(netflix_clean)

#创建图表保存文件
import os
if not os.path.exists('chart_'):
    os.makedirs('chart_') #不存在的话就创立chart文件夹
plt.figure(figsize=(12, 6)) #设置图表大小
platforms = list(platform_stats.keys()) #设置平台名列表
movie_counts = [platform_stats[p][1] for p in platforms] #各平台电影数
tv_counts = [platform_stats[p][2] for p in platforms] #各平台剧集数
#画堆叠柱状图：先画电影，再加剧集叠上面
plt.bar(platforms, movie_counts, label='Movies', color='#E50914')
plt.bar(platforms, tv_counts, bottom=movie_counts, label='TV Shows', color='#1428A0')
plt.title('Content Volume by Streaming Platform (Movie vs TV Show)')
plt.ylabel('Number of Contents') #图表美化加保存
plt.xlabel('Platform')
plt.legend() #显示图例
plt.savefig('chart_/content_type_count.png', dpi=300, bbox_inches='tight')  # Save high-res chart
plt.close()   #关闭画布，释放内存
#堆叠柱状图能同时展示各平台总内容数和电影  剧集的占比，普通柱状图只能对比电影 剧集的绝对数量，无法直观看到总和
plt.figure(figsize=(8, 8))#画饼图 正方形画布
genres = [g[0] for g in netflix_top5] 
counts = [g[1] for g in netflix_top5]
plt.pie(counts, labels=genres, autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)
plt.title('Netflix: Top 5 Popular Genres')
plt.savefig('chart_/netflix_top5_genres.png', dpi=300, bbox_inches='tight')
plt.close()
#合并4个平台清洗后的数据
all_clean_data = pd.concat([netflix_clean, amazon_clean, disney_clean, hulu_clean], ignore_index=True)
#筛选2010的数据，按年份加平台分组统计数量
yearly_trend = all_clean_data[all_clean_data['release_year'] >= 2010].groupby(['release_year', 'platform']).size().unstack(fill_value=0)

plt.figure(figsize=(14, 7))
for platform in yearly_trend.columns: #给平台画折线
    plt.plot(yearly_trend.index, yearly_trend[platform], marker='o', label=platform)
plt.title('Yearly Content Release Trend (2010-2023) by Platform')
plt.ylabel('Number of New Contents')
plt.xlabel('Release Year')
plt.legend()
plt.grid(True, alpha=0.3) #加网格（透明度0.3 不遮挡折现）
plt.savefig('chart_/yearly_content_trend.png', dpi=300, bbox_inches='tight')
plt.close()
#打印统计结果
print("=== Content Volume Statistics by Platform ===")
for p, (total, movie, tv) in platform_stats.items():
    movie_ratio = round(movie/total, 2)#电影占比 保留2位小数
    tv_ratio = round(tv/total, 2)#剧集占比
    print(f"{p}: Total {total} contents | Movies: {movie} ({movie_ratio}) | TV Shows: {tv} ({tv_ratio})")

print("\n=== Netflix: Top 5 Popular Genres ===")
for genre, count in netflix_top5:
    print(f"{genre}: {count} occurrences")

print("\n=== Analysis Complete! Charts saved to 'chart_' folder. ===")
