CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE user_stats (
  stat_id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(user_id),
  episodes_watched INT,
  minutes_watched INT,
  mean_score FLOAT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE genres (
  genre_id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(user_id),
  genre VARCHAR(50) NOT NULL,
  count INT NOT NULL
);

CREATE TABLE tags (
  tag_id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(user_id),
  tag VARCHAR(100) NOT NULL,
  count INT NOT NULL
);

CREATE TABLE scores (
  score_id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(user_id),
  score INT NOT NULL CHECK (score BETWEEN 1 AND 100),
  count INT NOT NULL
);

CREATE TABLE formats (
  format_id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(user_id),
  format VARCHAR(50) NOT NULL,
  count INT NOT NULL
);
