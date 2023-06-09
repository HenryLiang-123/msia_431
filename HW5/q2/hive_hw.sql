CREATE TABLE IF NOT EXISTS movie_ratings 
(
  user_id INT,
  movie_id INT,
  rating INT,
  time_stamp STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

LOAD DATA LOCAL INPATH '/home/public/movies' OVERWRITE INTO TABLE movie_ratings;

DROP VIEW IF EXISTS user_highly_rated_movies;

CREATE VIEW user_highly_rated_movies AS 
SELECT movie_id 
FROM movie_ratings 
WHERE user_id=1000 AND rating>3;

DROP VIEW IF EXISTS similar_users;

CREATE VIEW similar_users AS 
SELECT DISTINCT mr.user_id 
FROM movie_ratings mr
JOIN user_highly_rated_movies uhrm ON mr.movie_id = uhrm.movie_id
WHERE mr.rating>3 AND mr.user_id!=1000;

DROP VIEW IF EXISTS highly_rated_by_similar_users;

CREATE VIEW highly_rated_by_similar_users AS
SELECT mr.movie_id, COUNT(*) AS frequency 
FROM movie_ratings mr
JOIN similar_users su ON mr.user_id = su.user_id
WHERE mr.rating>3 
GROUP BY mr.movie_id;

SELECT hrbsu.movie_id, hrbsu.frequency
FROM highly_rated_by_similar_users hrbsu
LEFT OUTER JOIN user_highly_rated_movies uhrm ON hrbsu.movie_id = uhrm.movie_id
WHERE uhrm.movie_id IS NULL
ORDER BY hrbsu.frequency DESC 
LIMIT 10;
