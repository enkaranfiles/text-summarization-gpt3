import io
import os
from google.cloud import speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\Pc\Desktop\google-key\speechtotext-339819-3cd6af1fffe3.json'

client = speech.SpeechClient()
file_name = os.path.join(
    os.path.dirname(__file__),
    'sound-data',
    'conversation.mp3')

# Loads the audio into memory
with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding= speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
    sample_rate_hertz=16000,
    language_code='en-US')

response = client.recognize(config=config, audio=audio)

for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))