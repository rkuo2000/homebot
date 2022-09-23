# -*- coding: UTF-8 -*-

from fbchat import Client
from fbchat.models import *

client = Client('user_email', 'user_password')

# Fetches a list of all users you're currently chatting with, as `User` objects
users = client.fetchAllUsers()

for user in users:
   print("name={}, ID={}".format(user.name, user.uid) )
