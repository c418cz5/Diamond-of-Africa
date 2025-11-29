-- This code is manually written, no AI assistance used
-- Step 1: Create 5 tables 
CREATE TABLE IF NOT EXISTS director (
    director_id INT PRIMARY KEY AUTO_INCREMENT,
    director_name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS genre (
    genre_id INT PRIMARY KEY AUTO_INCREMENT,
    genre_name VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS actor (
    actor_id INT PRIMARY KEY AUTO_INCREMENT,
    actor_name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS content (
    content_id INT PRIMARY KEY AUTO_INCREMENT,
    show_id VARCHAR(50) NOT NULL UNIQUE,
    platform VARCHAR(20) NOT NULL CHECK (platform IN ('Netflix', 'Hulu')),
    type VARCHAR(20) NOT NULL CHECK (type IN ('Movie', 'TV Show')),
    title VARCHAR(200) NOT NULL,
    director_id INT NULL,
    release_year INT NOT NULL,
    rating VARCHAR(20) NULL,
    duration VARCHAR(50) NULL,
    description TEXT NULL,
    FOREIGN KEY (director_id) REFERENCES director(director_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS content_genre (
    content_genre_id INT PRIMARY KEY AUTO_INCREMENT,
    content_id INT NOT NULL,
    genre_id INT NOT NULL,
    FOREIGN KEY (content_id) REFERENCES content(content_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    UNIQUE KEY uk_content_genre (content_id, genre_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Step 2: Insert 1 record into each table 
INSERT INTO director (director_name, country)
VALUES ('Steven Spielberg', 'United States');

INSERT INTO genre (genre_name)
VALUES ('Action & Adventure');

INSERT INTO actor (actor_name, country)
VALUES ('Leonardo DiCaprio', 'United States');

INSERT INTO content (show_id, platform, type, title, director_id, release_year, rating, duration, description)
VALUES ('s42', 'Netflix', 'Movie', 'Jaws', 1, 1975, 'PG', '124 min', 'A great white shark terrorizes Amity Island');

INSERT INTO content_genre (content_id, genre_id)
VALUES (1, 1);