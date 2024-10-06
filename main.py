from ibm_watson import TextToSpeechV1
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

#text to speech api/url
url = 'https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/535507f1-3e96-48ee-8ef1-860a70aa6888'
apikey = 'tbaNhfKLNJXDNShVRW7gVZ0RrjOErVhG6C5cBgH_EL75'

#speech to test api/url
STTurl = 'https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/094f1f6b-7a40-412f-838c-649a9dff7f76'
STTapikey = 'KSxHhEgPDTCRaY3D-kN-OAwPHlFrwJYl__sP6xtd1tRA'

#text to speech section
# ---------------------------------------------------------------------
# authenticator = IAMAuthenticator(apikey)
# tts = TextToSpeechV1(authenticator=authenticator)
# tts.set_service_url(url)

# speaking from given prompt and saving into new audio file
# with open('./speak.mp3', 'wb') as audio_file:
#     res = tts.synthesize('Hi Tyler!', accept = 'audio/mp3', voice = 'en-US_AllisonV3Voice').get_result()
#     audio_file.write(res.content)

# speaking from txt file and saving into new audio file
# with open('./prompt.txt', 'r') as file:
#     text = file.readlines()
# text = [line.replace('\n', '') for line in text]
# text = ''.join(str(line) for line in text)
# with open('./speak.mp3', 'wb') as audio_file:
#     resFile = tts.synthesize(text, accept = 'audio/mp3', voice = 'en-US_AllisonV3Voice').get_result()
#     audio_file.write(resFile.content)

# ---------------------------------------------------------------------


#speech to text section
# ---------------------------------------------------------------------
STTauthenticator = IAMAuthenticator(STTapikey)
stt = SpeechToTextV1(authenticator=STTauthenticator)
stt.set_service_url(STTurl)

with open('./listen.mp3', 'rb') as f:
    sttres = stt.recognize(audio=f, content_type='audio/mp3', model='en-AU_Telephony').get_result()
    #sttres = stt.recognize(audio=f, content_type='audio/wav', timestamps=True, word_confidence=True).get_result()
    #sttres = stt.recognize(f, timestamps=True, content_type='audio/wav', inactivity_timeout=-1, word_confidence=True).get_result()

sttText = sttres['results'][0]['alternatives'][0]['transcript']
print(sttText)

