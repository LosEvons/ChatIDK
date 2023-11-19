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

# How to set up (notes for self)
1. Make sure you have Python3, venv and postgresql on your system
2. Create a python venv in the project folder
3. ``` pip install -r requirements.txt ```
4. ``` psql < schema.sql ```
5. Create a .env file, or otherwise define a DATABASE_URL and a SECRET_KEY.
6. Should work wheen ran in venv?

# Progress
Currently the application has working credential management and chat management. Currently not live updating or handling images. Style was copied from another project, and will very likely be left out of the
project in the interest of saving time and resources, as well as to compensate for huge motivation loss caused by working on it. Multiple rewrites have left the abstractions in a satisfactory state, and while I'd love to rewrite it at least once more, I'll refrain from doing so to shift focus to preferrable features.
