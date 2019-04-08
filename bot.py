import tweepy
import time

print("Bot de twitter")


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


def get_Solution(mention):
    api = twitter_api()
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
            Solucion = respuesta[1]
    return Solucion


def store_ganador_id(last_id):
    f_write = open("ganador.txt", "w")
    f_write.write(str(last_id))
    f_write.close()


def reply_to_tweets():
    try:
        api = twitter_api()
        print("Escribiendo replies...", flush=True)
        last_id = return_last_id()
        mentions = api.mentions_timeline(last_id)
        for mention in mentions:
            time.sleep(5)
            # print(str(mention.id) + ' - ' + mention.text, flush = True)
            last_seen_id = mention.id
            store_last_seen_id(last_seen_id)
            if str(get_Solution(mention)) in mention.text.lower():
                print("Solución encontrada", flush=True)
                print("Respondiendo...", flush=True)
                api.update_status(
                    "@" + mention.user.screen_name + "¡Respuesta correcta!", mention.id
                )
            else:
                print("Solución no encontrada", flush=True)
                print("Respondiendo...", flush=True)
                api.update_status(
                    "@" + mention.user.screen_name + "¡Respuesta incorrecta!",
                    mention.id,
                )

    except tweepy.error.TweepError:
        pass


while True:
    reply_to_tweets()
    time.sleep(30)
# mentions = api.mentions_timeline()
# for mention in mentions:
#   print(str(mention.id) + ' - ' + mention.text)
