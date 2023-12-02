CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, visible BOOLEAN);
CREATE TABLE chats (id SERIAL PRIMARY KEY, user1_id INTEGER, user2_id INTEGER);
CREATE TABLE messages (id SERIAL PRIMARY KEY, user_id INTEGER, chat_id INTEGER, content TEXT, created_at TIMESTAMP);
CREATE TABLE files (id SERIAL PRIMARY KEY, filepath TEXT);
CREATE TABLE attachments (id SERIAL PRIMARY KEY, file_id INTEGER, message_id INTEGER);