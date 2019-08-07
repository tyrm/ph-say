import boto3
import playsound

# Synthesize the sample text, saving it in an MP3 audio file
polly_client = boto3.client('polly')
response = polly_client.synthesize_speech(VoiceId='Brian',
                                          Engine='neural',
                                          OutputFormat='mp3',
                                          Text='This is sample text to synthesize.')
with open('speech.mp3', 'wb') as file:
    file.write(response['AudioStream'].read())

playsound.playsound('speech.mp3', True)
