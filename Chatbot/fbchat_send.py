# -*- coding: UTF-8 -*-

from fbchat import Client
from fbchat.models import *

image_url = "https://images-na.ssl-images-amazon.com/images/I/61r%2BHqg7NuL._SY355_.jpg"

client = Client("user_name", "user_password")

# user fbchat_basic.py to find friend's uid, or browser-check on title of messenging friend window
thread_id = 'friend_uid'

#thread_type = ThreadType.GROUP
thread_type = ThreadType.USER

# To send a message to the thread
client.send(Message(text='message from homebot'), thread_id=thread_id, thread_type=thread_type)

# To send the default `like` emoji
client.send(Message(emoji_size=EmojiSize.LARGE), thread_id=thread_id, thread_type=thread_type)

# To send a local image located at `<image path>`
client.sendLocalImage('robelf.png', message=Message(text='send a local image'), thread_id=thread_id, thread_type=thread_type)

# To send a remote image located at `<image url>`
client.sendRemoteImage(image_url, message=Message(text='send a remote image'), thread_id=thread_id, thread_type=thread_type)

# FB Logout 
client.logout()

