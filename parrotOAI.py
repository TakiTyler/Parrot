import sys
from openai import OpenAI
import keyboard
import time
import pyaudio
import wave

# declare and run the ai up here

'''
client = OpenAI()

messages = [
    {"role": "system", "content": "You are a talking parrot companion named polly who loves to teach."}
]

print(response.choices[0].message.content)
'''

print("AI IS NOW OPERATIONAL")

# loop for detecting the key press of 's' to start
while True:
    try:
        if keyboard.is_pressed('s'):  # if key 'q' is pressed
            print("The Parrot is now talking. Have fun!")
            break  # finishing the loop
    except:
        break

# Play an audio that the parrot is now listening


buffer_frames = 3200
formating = pyaudio.paInt16
rates = 16000

audio = pyaudio.PyAudio()

stream = audio.open(
    format = formating,
    channels = 1,
    rate = rates,
    input = True,
    frames_per_buffer = buffer_frames

)

print("NOW RECORDING")

seconds = int(rates/buffer_frames*5)
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

# Listen to the mic

# Figure out how to stop listening when we're quiet

    # If we can't figure it out, use a keypress to tell the computer that we're done

'''
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.7,
    max_tokens=50,
)
'''

# ORDER OF COMMANDS

# speech input

    # wait for a keypress to initiate

    # have a startup message?

# speech -> text

    # after it's done initiating, we allow for the computer mic to listen to audio

    # use something to read the audio file and translate it to text

# load openai with prompt to train it

    # this can happen anywhere, it just has to happen BEFORE the ai reads

# have openai read and respond to the prompt that was sent

    # this part is pretty much complete

    # a string will be returned of what the ai says

# transfer the text to ibm / openai to translate into speech

    #

# audio is played from computer

    # at the same time, the parrot starts to move its mouth

    # figure out how to start the arduino when we get the audio file

# loop back to the beginning

