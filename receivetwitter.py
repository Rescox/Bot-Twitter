#!/usr/bin/env python
import pika
import tweepy


def twitter_api():
    CONSUMER_KEY = ""
    CONSUMER_SECRET = ""
    ACCESS_KEY = ""
    ACCESS_SECRET = ""

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    print("hola")
    return api


connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()


channel.queue_declare(queue="hello")


def return_last_id():
    f_read = open("ultimotweet.txt", "r")
    last_id = int(f_read.read().strip())
    f_read.close()
    return last_id


def store_last_seen_id(last_id):
    f_write = open("ultimotweet.txt", "w")
    f_write.write(str(last_id))
    f_write.close()


def get_Solution(mention, api):
    # Sacamos el id de la pregunta y el texto del tweet al que se refiere
    print("El texto del tweet: " + mention.text)
    print("se refiere al tweet escrito en")
    print(mention.in_reply_to_status_id)
    # Devuelve el status (cosas del tweet)de un tweet
    tweet = api.get_status(mention.in_reply_to_status_id)
    aPregunta = tweet.text.split("-")  # Imprime el texto
    sPregunta = aPregunta[0]
    # Buscamos ahora en el .txt la solucion.
    print("-----------------------------------")
    print(sPregunta)
    fFile = open("soluciones.txt", "r").read()
    Solucion = -1
    aSolucion = fFile.splitlines()
    for i in aSolucion:
        respuesta = i.split("-")
        if respuesta[0] == sPregunta:
            print(respuesta)
            print("asdasd")
            Solucion = respuesta[1]
    print(Solucion)
    return Solucion


def callback(ch, method, properties, body):
    try:
        api = twitter_api()
        tweet = api.get_status(int(body))
        print(tweet.text)
        if str(get_Solution(tweet, api)) in tweet.text.lower():
            api.update_status(
                "@" + tweet.user.screen_name + "¡Respuesta correcta!", tweet.id
            )
        else:
            api.update_status(
                "@" + tweet.user.screen_name + "¡Respuesta incorrecta!", tweet.id
            )

        # if str(get_Solution(body)) in body.text.lower():
        # print("Solución encontrada", flush=True)
        # print("Respondiendo...", flush=True)
        # api.update_status(
        #    "@" + mention.user.screen_name + "¡Respuesta correcta!", mention.id
        # )
        # print(" [x] Received %r" % body)

    except tweepy.error.TweepError:
        pass


channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()

