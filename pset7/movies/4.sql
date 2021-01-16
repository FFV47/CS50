SELECT COUNT(*) FROM ratings
JOIN movies ON movies.id = ratings.movie_id
WHERE rating = 10
