import tweepy 
import markovify
import random
import os
import imghdr

import json
import urllib.request

from time import sleep
from nltk.corpus import genesis
from googleapiclient.discovery import build


from credentials import *


# Get genesis corpus
# data = genesis.words('english-web.txt')

text = genesis.open('english-web.txt')

# Build the model
text_model = markovify.Text(text)

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)

word0 = 'Genesis'
word1 = 'God'

words = ['Adam', 'Cain', 'Abel', 'Noah', 'Abram', 'Sarah', 'Lot', 'Melchizedek', 'Abraham', 
		'Isaac', 'Esau', 'Jacob', 'Rachel', 'Israel', 'Judah','Joseph']

# word2 = 'Isaac'
word2 = words[random.randint(0, 15)]

# update a status with text
# random_sentence = text_model.make_sentence()
start1 = text_model.make_sentence_with_start(word1)
start2 = text_model.make_sentence_with_start(word2)

start = start1 + '...\n    And ' + start2 + f'\n #{word0} #{word1} #{word2}'

print(start)

# retrive a random image from google engine using two words
q = word0 + word1 + word2
request = urllib.request.Request('https://www.googleapis.com/customsearch/v1?key=' 
	+ API_KEY + '&cx=' + SEARCH_ENGINE_ID + '&q=' + q + '&searchType=image')

with urllib.request.urlopen(request) as f:
    data = f.read().decode('utf-8')
   
data = json.loads(data)
results = data['items']
url = random.choice(results)['link']
urllib.request.urlretrieve(url, './imagi')
imagetype = imghdr.what('./imagi')

try:
	os.rename('imagi', 'imagi.' + imagetype)
except IOError:
    print('An error occured trying to read the file\'s type.')

api.update_with_media('imagi.' + imagetype, start)


# update status every 10 minutes
# for i in range(100):
	# sleep(600)



