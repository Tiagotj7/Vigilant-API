CREATE TABLE targets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  url TEXT
);

CREATE TABLE metrics (
  id INT AUTO_INCREMENT PRIMARY KEY,
  target_id INT,
  status INT,
  response_time FLOAT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);