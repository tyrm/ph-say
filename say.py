import os
import boto3
import pygame
from flask import Flask, request
from redis import StrictRedis
from redis_lock import Lock

app = Flask(__name__)


def say(speech_text):
    redis_host = os.getenv('REDIS_HOST', "127.0.0.1")
    conn = StrictRedis(host=redis_host)

    # Synthesize the sample text, saving it in an MP3 audio file
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(VoiceId='Matthew',
                                              Engine='neural',
                                              OutputFormat='mp3',
                                              Text=speech_text)

    with Lock(conn, "talking"):
        with open('speech.mp3', 'wb') as file:
            file.write(response['AudioStream'].read())

        print("Got the lock. Doing some work ...")

        pygame.mixer.init()
        pygame.mixer.music.load("speech.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy() == True:
            continue

        os.remove("speech.mp3")

def newscast(speech_text):
    redis_host = os.getenv('REDIS_HOST', "127.0.0.1")
    conn = StrictRedis(host=redis_host)

    # Synthesize the sample text, saving it in an MP3 audio file
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(VoiceId='Matthew',
                                              Engine='neural',
                                              OutputFormat='mp3',
                                              Text='<speak><amazon:domain name="news">{0}</amazon:domain></speak>'.format(speech_text),
                                              TextType='ssml')

    with Lock(conn, "talking"):
        with open('speech.mp3', 'wb') as file:
            file.write(response['AudioStream'].read())

        print("Got the lock. Doing some work ...")

        pygame.mixer.init()
        pygame.mixer.music.load("speech.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy() == True:
            continue

        os.remove("speech.mp3")

@app.route('/')
def hello_world():
    # here we want to get the value of user (i.e. ?user=some-value)
    speech_text = request.args.get('s')
    news_text = request.args.get('n')
    if speech_text is not None:
        say(speech_text)
    elif news_text is not None:
        newscast(news_text)

    return 'ok!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
