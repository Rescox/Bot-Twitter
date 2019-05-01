#!/usr/bin/env python
import pika
import tweepy
import time


def twitter_api():
    CONSUMER_KEY = ""
    CONSUMER_SECRET = ""
    ACCESS_KEY = "-"

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    print("Conectando a twitter")
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


def reply_to_tweets():
    try:
        api = twitter_api()
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        channel = connection.channel()
        print("Escribiendo replies...", flush=True)
        last_id = return_last_id()
        mentions = api.mentions_timeline(last_id)
        channel.queue_declare(queue="hello")
        print(mentions)
        for mention in mentions:
            time.sleep(1)
            channel.basic_publish(
                exchange="", routing_key="hello", body=str(mention.id)
            )
            print(str(mention.id) + " - " + mention.text, flush=True)
            last_seen_id = mention.id
            store_last_seen_id(last_seen_id)

    except tweepy.error.TweepError:
        print("asdasdasd")
    connection.close


reply_to_tweets()
