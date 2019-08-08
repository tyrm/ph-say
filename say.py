from flask import Flask, request
import boto3
import os
import playsound
from redis import StrictRedis
from redis_lock import Lock

app = Flask(__name__)


def say(speech_text):
    redis_host = os.getenv('REDIS_HOST', "127.0.0.1")
    conn = StrictRedis(host=redis_host)

    # Synthesize the sample text, saving it in an MP3 audio file
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(VoiceId='Brian',
                                              Engine='neural',
                                              OutputFormat='mp3',
                                              Text=speech_text)

    with Lock(conn, "talking"):
        with open('speech.mp3', 'wb') as file:
            file.write(response['AudioStream'].read())

        print("Got the lock. Doing some work ...")
        playsound.playsound('speech.mp3', True)
        os.remove("speech.mp3")


@app.route('/')
def hello_world():
    # here we want to get the value of user (i.e. ?user=some-value)
    speech_text = request.args.get('s')
    if speech_text is not None:
        say(speech_text)

    return 'ok!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
