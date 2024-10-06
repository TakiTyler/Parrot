from ibm_watson import TextToSpeechV1
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
import sys
from openai import OpenAI
import keyboard
import time
import pyaudio
import wave
from pydub import AudioSegment
from playsound import playsound
import speech_recognition as sr

#text to speech api/url
url = 'https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/535507f1-3e96-48ee-8ef1-860a70aa6888'
apikey = 'tbaNhfKLNJXDNShVRW7gVZ0RrjOErVhG6C5cBgH_EL75'

#speech to test api/url
STTurl = 'https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/094f1f6b-7a40-412f-838c-649a9dff7f76'
STTapikey = 'KSxHhEgPDTCRaY3D-kN-OAwPHlFrwJYl__sP6xtd1tRA'



def listenToSpeech():
    buffer_frames = 3200
    formating = pyaudio.paInt16
    rates = 16000  # Might change this to 44100 to match with CD standards

    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=formating,
        channels=1,
        rate=rates,
        input=True,
        frames_per_buffer=buffer_frames
    )

    print("NOW RECORDING")

    # Calculating how long we record for (multiplying the buffer_frames gives us the time in seconds)
    seconds = int(rates / buffer_frames * 5)

    # Frames will store the audio data as we are looping, eventually being turned into a .wav file
    frames = []

    # Recording audio for the amount of seconds we have
    for i in range(0, seconds):
        data = stream.read(buffer_frames)
        frames.append(data)
        if keyboard.is_pressed('c'):
            print("Ended early")
            break

    # Ending the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Creating the wav file
    obj = wave.open("listen.wav", "wb")
    obj.setnchannels(1)
    obj.setsampwidth(audio.get_sample_size(formating))
    obj.setframerate(rates)
    obj.writeframes(b"".join(frames))
    obj.close()

    return

# text to speech section
# ---------------------------------------------------------------------
def TTS(pollyInput):
    authenticator = IAMAuthenticator(apikey)
    tts = TextToSpeechV1(authenticator=authenticator)
    tts.set_service_url(url)

    # speaking from given prompt and saving into new audio file
    with open('./speak.wav', 'wb') as audio_file:
        res = tts.synthesize(pollyInput, accept = 'audio/wav', voice = 'en-US_AllisonV3Voice').get_result()
        audio_file.write(res.content)

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
def STT():
    STTauthenticator = IAMAuthenticator(STTapikey)
    stt = SpeechToTextV1(authenticator=STTauthenticator)
    stt.set_service_url(STTurl)

    with open('./listen.wav', 'rb') as f:
        sttres = stt.recognize(audio=f, content_type='audio/wav', model='en-AU_Telephony').get_result()
    sttText = sttres['results'][0]['alternatives'][0]['transcript']
    return sttText

# ---------------------------------------------------------------------

def initializePolly():
    messages = [
        {"role": "system", "content": "You are a talking parrot named Polly. You're purpose is to be a chat bot that "
                                      "can interact with children in a helpful manner. When explaining anything, "
                                      "you have to explain as if you're talking to a third grader. But remember, "
                                      "you are a parrot. You cannot be too formal when speaking and must add a "
                                      "'squawk' at the start of your responses. Additionally, your language should be "
                                      "similar to that of a pirate, but still output coherent sentences, "
                                      "without being mean. Very rarely mention crackers. Limit your responses"
                                      "to four sentences. Squawk does not count as a sentence. Pause after each squawk."}
    ]

    return messages

# Function for sending the user's question to the openai API
def askPolly(messages, userInput):
    addMessages = {"role": "user", "content": userInput}

    messages.append(addMessages)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=100,
    )

    new_response = response.choices[0].message.content

    # new_response = new_response.replace("'", "")

    print("\nRESPONSE BELOW\n")

    return new_response

# Grabbing the audio file to modify
def increasePitch():
    audioFile = AudioSegment.from_wav('speak.wav')

    # Calculating how much we will increase the "sample rate" by
    increaseOctave = int(audioFile.frame_rate * 1.2)

    # Audio apparently becomes strange after changing the pitch, this fixes it
    newAudio = audioFile._spawn(audioFile.raw_data, overrides={'frame_rate': increaseOctave})

    # Converting sample rate
    newAudio = newAudio.set_frame_rate(44100)  # may change this to 16000 depending on variable: rates

    newAudio.export("actuallySpeak.wav", format="wav")

    # Deleting the old file
    os.remove('listen.wav')
    os.remove('speak.wav')

    return

# audio is played from computer

# at the same time, the parrot starts to move its mouth

# figure out how to start the arduino when we get the audio file

## MAIN

print("AI IS NOW OPERATIONAL")

client = OpenAI()

inputMessages = initializePolly()

print("Press S to start")

continueLoop = 'y'


while continueLoop != 'n':
    # loop for detecting the key press of 's' to start
    while True:
        try:
            if keyboard.is_pressed('s'):
                print("The Parrot is now talking. Have fun!")
                break  # finishing the loop
        except:
            break

    try:




        listenToSpeech()

        # Add the audio recording
        userInput = STT()
        print(userInput)

        pollyOut = askPolly(messages=inputMessages, userInput=userInput)
        print(pollyOut)

        # pollyOut = ("Squawk! Eight planets there be in our solar system, arrr! From the closest to the sun, they be Mercury, Venus (Earth's sister!), Earth, Mars, Jupiter, Saturn, Uranus, and Neptune.")
        TTS(pollyInput=pollyOut)

        # increasing the pitch of the audio to make it sound more "bird-like"
        increasePitch()

        # Automatically play the sound
        playsound(r'C:\Users\takim\OneDrive\Documents\GitHub\Parrot\actuallySpeak.wav')

        # Asking the user if they would like to ask polly another question
        continueLoop = input("Would you like to ask another question? (y/n): ")

        # Ensuring either y or Y works
        continueLoop = continueLoop.lower()
    except:
        # Catch-all error in case anything goes wrong
        pollyError = "I couldn't quite hear you, squawk! Please ask me again."

        # Make the parrot say something went wrong
        TTS(pollyInput=pollyError)

        increasePitch()

        playsound(r'C:\Users\takim\OneDrive\Documents\GitHub\Parrot\actuallySpeak.wav')

        continueLoop = input("Would you like to ask another question? (y/n): ")

        continueLoop = continueLoop.lower()
        continue


# Make the listening to audio process smoother
    # After a certain amount of time, stop the recording
    # Up to a maximum of... 10 seconds?
