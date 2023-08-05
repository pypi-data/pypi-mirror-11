GjertsenTweet
=============

GjertsenTweet is a simple twitter client built with npyscreen. It lets you
access twitter from your terminal so you can post tweets, read tweets and search 
for tweets.

.. image:: http://i.imgur.com/t3bofl5.png

Installation
------------

pip install gjertsentweet

For windows user, note that you need to install curses from here
http://www.lfd.uci.edu/~gohlke/pythonlibs/ if you already havent done it

Build from source
-----------------
pip install -r requirements.txt

then run **python setup.py install**

or just run client.py

Usage
-----
Run *gjertsentweet* in your terminal to fire it up, commandline-arguments doesn't
exist in this app.

When launched for the first time you will be asked to open a link in your browser
in order to approve the app. You will be given a pin from twitter which lets 
you log into your account from GjertsenTweet.

When logged in, you can simply use the arrow keys or enter to move around.
Note that once you have moved down to feed, you can't use the arrow key to
move the cursor back to the tweet/search fields. To do this you will have to
press one of the buttons.

The twitter feed will be updated on the fly.

Note that you have to press enter when the dialog boxes pops up in order
to move the cursor down to the button/buttons
