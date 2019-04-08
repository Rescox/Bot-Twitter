#!/usr/bin/env python
import pika
import tweepy


def twitter_api():
    CONSUMER_KEY = "FCVYt7lC1jlFTt8s0HxU0K4g3"
    CONSUMER_SECRET = "Tt2MUUSMd9hP75AMUqWLziqrNRngjWB9y4Na7HhhuZRD3d2ibI"
    ACCESS_KEY = "1063814327587799041-6rmZ9wMrhMD5cWcSAd0ANMgsV2ZPGl"
    ACCESS_SECRET = "b8sxtICZo2D3XyTE5KrQx0Y9soVRrfXnWg81fuGG9nSVa"

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    print("hola")
    return api


def return_last_id():
    f_read = open("ultimotweet.txt", "r")
    last_id = int(f_read.read().strip())
    f_read.close()
    return last_id


def store_last_seen_id(last_id):
    f_write = open("ultimotweet.txt", "w")
    f_write.write(str(last_id))
    f_write.close()


api = twitter_api()
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

last_id = return_last_id()
mentions = api.mentions_timeline(last_id)
mentions = mentions[1:]
channel.queue_declare(queue="hello")
for mention in mentions:
    print(mention.text)
    channel.basic_publish(exchange="", routing_key="hello", body=mention.text)
    print(" [x] Sent 'Hello World!'")
    last_seen_id = mention.id
    print(last_seen_id)
    store_last_seen_id(last_seen_id)
connection.close
