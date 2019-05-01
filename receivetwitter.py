#!/usr/bin/env python
import pika
import tweepy


def twitter_api():
    CONSUMER_KEY = ""
    CONSUMER_SECRET = ""
    ACCESS_KEY = "-"
    ACCESS_SECRET = ""

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    print("hola")
    return api


connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()


channel.queue_declare(queue="hello")


def get_Solution(mention, api):
    # Sacamos el id de la pregunta y el texto del tweet al que se refiere
    print("El texto del tweet: " + mention)
    # Devuelve el status (cosas del tweet)de un tweet
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
            Solucion = respuesta[1]
    return Solucion


def callback(ch, method, properties, body):
    api = twitter_api()
    tweet = api.get_status(int(body))
    print(tweet.text)
    
    # if str(get_Solution(body)) in body.text.lower():
    # print("Solución encontrada", flush=True)
    # print("Respondiendo...", flush=True)
    # api.update_status(
    #    "@" + mention.user.screen_name + "¡Respuesta correcta!", mention.id
    # )
    print(" [x] Received %r" % body)


channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=False)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()

