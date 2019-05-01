import tweepy
import time


def remove_char(s):
    return s[: len(s) - 1]


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


def take_image(i):
    cadena = "P"
    print(cadena)
    cadena += i.__str__()
    # cadena = remove_char(cadena)
    print("img/" + cadena + ".jpeg")
    return cadena


def upload_image():
    i = 4
    api = twitter_api()
    while True:
        sFoto = take_image(i)
        api.update_with_media(
            "img/" + sFoto + ".jpeg", status=sFoto[1] + "-Puzle de la Villa Misteriosa"
        )
        time.sleep(3600 * 12)
        i += 1


upload_image()
