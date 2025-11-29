# Table Schemas (5 Tables, 1 Association Class)
## 1. Table: director (Entity Table)
| Column Name   | Data Type    | Constraints          | Description                  |
|---------------|--------------|----------------------|------------------------------|
| director_id   | INT          | PK, AUTO_INCREMENT   | Unique ID for director       |
| director_name | VARCHAR(100) | NOT NULL             | Full name of director        |
| country       | VARCHAR(50)  | NULL                 | Nationality of director      |

## 2. Table: genre (Entity Table)
| Column Name | Data Type    | Constraints          | Description                  |
|-------------|--------------|----------------------|------------------------------|
| genre_id    | INT          | PK, AUTO_INCREMENT   | Unique ID for genre          |
| genre_name  | VARCHAR(50)  | NOT NULL, UNIQUE     | Name of genre (e.g., Comedy) |

## 3. Table: actor (Entity Table)
| Column Name | Data Type    | Constraints          | Description                  |
|-------------|--------------|----------------------|------------------------------|
| actor_id    | INT          | PK, AUTO_INCREMENT   | Unique ID for actor          |
| actor_name  | VARCHAR(100) | NOT NULL             | Full name of actor           |
| country     | VARCHAR(50)  | NULL                 | Nationality of actor         |

## 4. Table: content (Core Entity Table)
| Column Name   | Data Type    | Constraints          | Description                  |
|---------------|--------------|----------------------|------------------------------|
| content_id    | INT          | PK, AUTO_INCREMENT   | Unique ID for content        |
| show_id       | VARCHAR(50)  | NOT NULL, UNIQUE     | Original ID from platform    |
| platform      | VARCHAR(20)  | NOT NULL             | Netflix / Hulu               |
| type          | VARCHAR(20)  | NOT NULL             | Movie / TV Show              |
| title         | VARCHAR(200) | NOT NULL             | Title of content             |
| director_id   | INT          | FK → director        | Link to director table       |
| release_year  | INT          | NOT NULL             | Year of release              |
| rating        | VARCHAR(20)  | NULL                 | Content rating (e.g., PG)    |
| duration      | VARCHAR(50)  | NULL                 | Duration (e.g., 120 min)     |
| description   | TEXT         | NULL                 | Content description          |

## 5. Table: content_genre (Association Class)
| Column Name       | Data Type | Constraints          | Description                  |
|-------------------|-----------|----------------------|------------------------------|
| content_genre_id  | INT       | PK, AUTO_INCREMENT   | Unique ID for association    |
| content_id        | INT       | FK → content, NOT NULL | Link to content table      |
| genre_id          | INT       | FK → genre, NOT NULL | Link to genre table          |
| UNIQUE KEY        | -         | (content_id, genre_id) | Avoid duplicate links    |