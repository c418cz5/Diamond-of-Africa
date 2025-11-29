# Streaming Platform Analysis Report (Netflix & Hulu)
## 1. Introduction
This report analyzes content data from Netflix and Hulu
## 2. Data & Methodology
- Datasets: `netflix_titles.csv`, `hulu_titles.csv`
- Tools: Python (pandas/matplotlib), MySQL, Draw.io
- Normalization: The dataset is normalized to 3NF (5 tables, 1 association class) to eliminate data redundancy.

## 3. Domain Model & 3NF Normalization
### 3.1 Domain Model Diagram
The domain model includes 4 entities (Content, Director, Genre, Actor) and 1 association class (Content_Genre) to represent many-to-many relationships between Content and Genre.

### 3.2 3NF Normalization Result
- 1NF: Split multi-valued attributes (listed_in, cast) into separate tables.
- 2NF: Eliminate partial dependencies (split director info into `director` table).
- 3NF: Eliminate transitive dependencies (split actor info into `actor` table).
- Final tables: `content`, `director`, `genre`, `actor`, `content_genre`.
## 4. Key Analysis Results
### 4.1 Content Type Distribution
| Platform | Movie | TV Show | Total |
|----------|-------|---------|-------|
| Netflix  | 6131  | 2676    | 8807  |
| Hulu     | 1484  | 1589    | 3073  |
- Netflix has more total content (8807 vs 3073) and focuses on movies (70% of total).
- Hulu is the only platform where TV shows account for more than 50% of total content.

### 4.2 Netflix Top 5 Genres
1. International Movies (2752 occurrences)
2. Dramas (2427 occurrences)
3. Comedies (1674 occurrences)
4. Action & Adventure (859 occurrences)
5. Documentaries (829 occurrences)

## 5. Conclusion
- Netflix should continue to strengthen international movies to maintain its advantage.
- Hulu can focus on TV shows to differentiate from other platforms.
- Normalizing the dataset to 3NF reduces data redundancy and improves data integrity.