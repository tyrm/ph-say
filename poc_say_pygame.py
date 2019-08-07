import boto3
import time
from pygame import mixer # Load the required library


# Synthesize the sample text, saving it in an MP3 audio file
polly_client = boto3.client('polly')
response = polly_client.synthesize_speech(VoiceId='Joanna',
                                          OutputFormat='mp3',
                                          Text='This is sample text to synthesize.')
with open('speech.mp3', 'wb') as file:
    file.write(response['AudioStream'].read())


mixer.init()
mixer.music.load('speech.mp3')
mixer.music.play()

time.sleep(5)
