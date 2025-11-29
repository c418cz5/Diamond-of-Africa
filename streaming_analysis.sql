CREATE TABLE streaming_content (
    content_id INT IDENTITY(1,1) PRIMARY KEY,  -- Unique content ID (auto-increment)
    show_id VARCHAR(50) UNIQUE,                -- Original platform content ID
    platform VARCHAR(20) NOT NULL,             -- Streaming platform (Netflix/Amazon Prime/Disney+/Hulu)
    type VARCHAR(20) NOT NULL,                 -- Content type (Movie/TV Show)
    title VARCHAR(200) NOT NULL,               -- Content title
    director VARCHAR(200) NULL,                -- Director (nullable)
    release_year INT NOT NULL,                 -- Release year (non-nullable)
    rating VARCHAR(20) NULL,                   -- Content rating (e.g., TV-MA/PG-13)
    listed_in VARCHAR(200) NULL                -- Genre tags (comma-separated)
);

SELECT 
    platform,
    COUNT(*) AS total_content,
    SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS movie_count,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_show_count,
    ROUND(SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END)*1.0/COUNT(*), 2) AS movie_ratio,
    ROUND(SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END)*1.0/COUNT(*), 2) AS tv_show_ratio
FROM streaming_content
GROUP BY platform;


SELECT 
    release_year,
    SUM(CASE WHEN platform = 'Netflix' THEN 1 ELSE 0 END) AS netflix_count,
    SUM(CASE WHEN platform = 'Amazon Prime' THEN 1 ELSE 0 END) AS amazon_count,
    SUM(CASE WHEN platform = 'Disney+' THEN 1 ELSE 0 END) AS disney_count,
    SUM(CASE WHEN platform = 'Hulu' THEN 1 ELSE 0 END) AS hulu_count
FROM streaming_content
WHERE release_year >= 2010 AND release_year <= 2023
GROUP BY release_year
ORDER BY release_year ASC;

WITH disney_genres AS (
    SELECT 
        SUBSTRING(listed_in, 1, CHARINDEX(',', listed_in + ',') - 1) AS genre
    FROM streaming_content
    WHERE platform = 'Disney+' AND listed_in IS NOT NULL
    UNION ALL
    SELECT 
        SUBSTRING(
            listed_in, 
            CHARINDEX(',', listed_in) + 2, 
            LEN(listed_in) - CHARINDEX(',', listed_in) + 1
        ) AS genre
    FROM streaming_content
    WHERE platform = 'Disney+' AND listed_in IS NOT NULL AND CHARINDEX(',', listed_in) > 0
)
SELECT TOP 5
    genre,
    COUNT(*) AS genre_count
FROM disney_genres
GROUP BY genre
ORDER BY genre_count DESC;


SELECT 
    platform,
    SUM(CASE WHEN rating IN ('TV-MA', 'R', 'NC-17') THEN 1 ELSE 0 END) AS adult_content,
    SUM(CASE WHEN rating IN ('TV-G', 'G', 'PG', 'TV-PG') THEN 1 ELSE 0 END) AS family_content,
    ROUND(SUM(CASE WHEN rating IN ('TV-MA', 'R', 'NC-17') THEN 1 ELSE 0 END)*1.0/COUNT(*), 2) AS adult_ratio
FROM streaming_content
WHERE rating IS NOT NULL
GROUP BY platform;

