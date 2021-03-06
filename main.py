# -*- coding: utf-8 -*-
from User import User 
from Config import Config
from Liker import Liker

print ''

# INSTAGRAM USER INFORMATION

client_user 	= 'your client_user'
client_id		= 'your client id'
access_token 	= 'your access_token'
client_secret 	= 'your client_secret'


# Choose the tag you want to like based on, keep the word in double
# quotes, do not put a # sign in front of the tag
search_tags = [ u'cat' ]

# filter media by languages, using langid.py
langs = [ u'en', u'pt']

# If in other to the media be liked it has to have another tag, list the possiblilities here
related_tags = [ u'blackcat', u'love', u'kitty' ]

# Don't like media that contains the string 'pussy' 
# Tags starting with the '*' will be tested as a substring
ignored_tags = [ u'*pussy', ]

# Media from those users won't be liked
ignored_users 	= [ u'emmadalla', u'feldsy' ]

# Array that stores all the configs
configs = []

# New user object
user = User( client_user = client_user, client_id = client_id, access_token = access_token, client_secret = client_secret )

# New config object
config = Config( search_tags = search_tags, langs = langs, related_tags = related_tags, ignored_tags = ignored_tags, ignored_users = ignored_users, config_user = user, max_iterations = 300 )
		
# Add the new config to the configs array
configs.append( config )

# New Liker
liker = Liker( min_interval = 130, max_interval = 143, configs = configs  )

# Seat back and relax
liker.make_likes()