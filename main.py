from keys import *
import tweepy
import time
import requests

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
  print('retrieving and replying to tweets...', flush=True)
  last_seen_id = retrieve_last_seen_id(FILE_NAME)
  mentions = api.mentions_timeline(
                      last_seen_id,
                      tweet_mode='extended')
  for mention in reversed(mentions):
      print(str(mention.id) + ' - ' + mention.full_text, flush=True)
      last_seen_id = mention.id

      tweet = mention.full_text
      movie_title = tweet.replace("@FilmBot3", "").lstrip()

      store_last_seen_id(last_seen_id, FILE_NAME)
      x = requests.get('http://www.omdbapi.com/?apikey=' + OMDB_PI_KEY + '&t=' + movie_title)
      response = x.json()
      title_n_year = response['Title'] + ' ' + response['Year']
      imdb = response['Ratings'][0]['Source'] + ': ' + response['Ratings'][0]['Value']
      rotten_tomatoes = response['Ratings'][1]['Source'] + ': ' + response['Ratings'][1]['Value']
      metacritic = response['Ratings'][2]['Source'] + ': ' + response['Ratings'][2]['Value']

      api.update_status('@' + mention.user.screen_name + ' ' + title_n_year + ' ' + imdb + ' ' + rotten_tomatoes + ' ' + metacritic, mention.id)

while True:
  reply_to_tweets()
  time.sleep(30)