'''
Created on Jun 27, 2018

@author: mark
'''
from instagram.client import InstagramAPI

api = InstagramAPI(client_id='markaltaweel', client_secret='prath4a5')
recent_media, next_ = api.user_recent_media()
photos = []
for media in recent_media:
    photos.append('<img src="%s"/>' % media.images['thumbnail'].url)