import os

import boto3
import pygame
from flask import Flask, request
from redis import StrictRedis
from redis_lock import Lock

app = Flask(__name__)


def say(speaker, speech_text):
    redis_host = os.getenv('REDIS_HOST', "127.0.0.1")
    conn = StrictRedis(host=redis_host)

    # Synthesize the sample text, saving it in an MP3 audio file
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(VoiceId=speaker,
                                              Engine='neural',
                                              OutputFormat='mp3',
                                              Text=speech_text)

    with Lock(conn, "talking"):
        print("Got the lock. Doing some work ...")

        pygame.mixer.init()
        pygame.mixer.music.load(response['AudioStream'])
        pygame.mixer.music.play()

        # Wait for Auudio to Finish
        while pygame.mixer.music.get_busy() == True:
            continue


def say_w_beep(speaker, speech_text):
    redis_host = os.getenv('REDIS_HOST', "127.0.0.1")
    conn = StrictRedis(host=redis_host)

    # Synthesize the sample text, saving it in an MP3 audio file
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(VoiceId=speaker,
                                              Engine='neural',
                                              OutputFormat='mp3',
                                              Text=speech_text)

    with Lock(conn, "talking"):
        print("Got the lock. Doing some work ...")

        pygame.mixer.init()

        pygame.mixer.music.load("beep.mp3")
        pygame.mixer.music.play()

        # Wait for Auudio to Finish
        while pygame.mixer.music.get_busy() == True:
            continue

        pygame.mixer.music.load(response['AudioStream'])
        pygame.mixer.music.play()

        # Wait for Auudio to Finish
        while pygame.mixer.music.get_busy() == True:
            continue


def newscast(speaker, speech_text):
    redis_host = os.getenv('REDIS_HOST', "127.0.0.1")
    conn = StrictRedis(host=redis_host)

    # Synthesize the sample text, saving it in an MP3 audio file
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(VoiceId=speaker,
                                              Engine='neural',
                                              OutputFormat='mp3',
                                              Text='<speak><amazon:domain name="news">{0}</amazon:domain></speak>'.format(
                                                  speech_text),
                                              TextType='ssml')

    with Lock(conn, "talking"):
        print("Got the lock. Doing some work ...")

        pygame.mixer.init()
        pygame.mixer.music.load(response['AudioStream'])
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy() == True:
            continue


@app.route('/matthew')
@app.route('/Matthew')
def matthew_say():
    # here we want to get the value of user (i.e. ?user=some-value)
    speech_text = request.args.get('s')
    speech_w_beep_text = request.args.get('sb')
    news_text = request.args.get('n')
    if speech_text is not None:
        say("Matthew", speech_text)
    elif news_text is not None:
        newscast("Matthew", news_text)
    elif speech_w_beep_text is not None:
        say_w_beep("Matthew", speech_w_beep_text)

    return 'ok!'


@app.route('/joanna')
@app.route('/Joanna')
def joanna_say():
    # here we want to get the value of user (i.e. ?user=some-value)
    speech_text = request.args.get('s')
    speech_w_beep_text = request.args.get('sb')
    news_text = request.args.get('n')
    if speech_text is not None:
        say("Joanna", speech_text)
    elif news_text is not None:
        newscast("Joanna", news_text)
    elif speech_w_beep_text is not None:
        say_w_beep("Joanna", speech_w_beep_text)

    return 'ok!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
