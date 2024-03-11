CREATE DOMAIN REQUEST_STATUS AS VARCHAR CHECK (
    value = 'pending' OR
    value = 'failure' OR
    value = 'ready' OR
    value = 'done'
);

CREATE TABLE IF NOT EXISTS requests (
    id SERIAL PRIMARY KEY,
    email VARCHAR(30) NOT NULL,
    status REQUEST_STATUS DEFAULT 'pending',
    song_id VARCHAR(150) DEFAULT NULL
);