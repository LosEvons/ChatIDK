# ChatIDK
A chat webapp made with Python3, Flask and PostrgreSQL.

The intention is to create a chatting app, where users can log in to an account and send and recieve messages from each other, that can include unicode characters, and possibly pictures and video.
Since I am unaware of my skills, I will provide a roadmap for features and classify them as nessecary, preferrable, and extra. Nessecary features must be completed for the app to be functional. 
Preferrable features improve the quality of life of the application and extra features make it unique. I've also commented for myself some important things to remember while implementing them.
1. Simple user database (will have to be broken down into discrete steps once I know what those are)
  - Pay clear attention to security and privacy concerns
  - Preferrable: password reset system
2. Two way chat connection
  - Preferrable: live updating
  - Preferrable: image previews (I'm guessing video previews would be easy to implement after this, but we will put that in the "extra" category for now.)
  - Extra: activity indicator
3. Style
  - Try to do it on the side, but don't get stuck while prototyping

I have a faint idea to develop a music sharing system into the application to make it unique, but since that will most likely lead to issues with copyright and licencing, it will be left on the backburner.
Similarly the current name of this repository and project is subject to change.

It's a prototype, until it isn't, and then we'll deal with the problems that come from that.

## Current State
The user may create an account, log into that account and send messages to other users. Those messages may contain text or files. The file sharing system is WIP, and I am uncertain as to how to proceed with it. I am very certain it is not safe right now, and probably shouldn't even be in the main branch in its current state. The user may also delete their account.

## Future
Next I am going to look into the file sharing system, and as to how I could improve it. I will also improve the style of the site, and perhaps add profile pictures if time allows.

# How to set up (notes for self)
**1.** Make sure you have Python3, venv and postgresql on your system. Clone this repository onto your machine, and start in the root folder.
**2.** In chatidk/config.py set your SECRET_KEY and SQLALCHEMY_DATABASE_URI.
```python
class Config:
    SECRET_KEY = <your secret key> 
    SQLALCHEMY_DATABASE_URI = <your database uri>
    ...

class TestConfig:
    SECRET_KEY = <your secret key>
    SQLALCHEMY_DATABASE_URI = <your database uri>
    ...
```
**3.** Create a python venv in the project folder
```bash
python3 -m venv venv
```
**4.** Enter the venv and install dependencies from requirements.txt
```bash
source venv/bin/activate
pip install -r requirements.txt
```
**5.** Make sure the following tables can be created in your database, and won't conflict with any existing ones. You might also want to consider creating a new database specifically for this program.
```sql
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, visible BOOLEAN);
CREATE TABLE chats (id SERIAL PRIMARY KEY, user1_id INTEGER, user2_id INTEGER);
CREATE TABLE messages (id SERIAL PRIMARY KEY, user_id INTEGER, chat_id INTEGER, content TEXT, created_at TIMESTAMP);
CREATE TABLE files (id SERIAL PRIMARY KEY, filepath TEXT);
CREATE TABLE attachments (id SERIAL PRIMARY KEY, file_id INTEGER, message_id INTEGER);
```
**6.** Create the tables specified in schema.sql in your database
```bash
psql < schema.sql
```
**7.** You should now be able to run the program with
```bash
flask --app chatidk run
```
