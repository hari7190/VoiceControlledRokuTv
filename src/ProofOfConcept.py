# Author : Harikrishnan
# Date: 12 Mar 2018


# import subprocess

import speech_recognition as sr

from pip._vendor import requests

# How to reach TV

url = 'http://192.168.1.8:8060/keypress/'
payload = {'key': 'val'}
headers = {}

# enter the name of usb microphone that you found using lsusb. In OSX system_profiler SPAudioDataType
# the following name is only used as an example

mic_name = "Built-in Microphone"

# Sample rate is how often values are recorded
sample_rate = 48000


# Chunk is like a buffer. It stores 2048 samples (bytes of data) here.
# it is advisable to use powers of 2 such as 1024 or 2048
chunk_size = 3096


# Initialize the recognizer
r = sr.Recognizer()


# generate a list of all audio cards/microphones
mic_list = sr.Microphone.list_microphone_names()

print(mic_list)

# the following loop aims to set the device ID of the mic that
# we specifically want to use to avoid ambiguity.
for i, microphone_name in enumerate(mic_list):
    if microphone_name == mic_name:
        device_id = i

# use the microphone as source for input. Here, we also specify
# which device ID to specifically look for incase the microphone
# is not working, an error will pop up saying "device_id undefined"
with sr.Microphone(device_index=device_id, sample_rate=sample_rate,
                   chunk_size=chunk_size) as source:
    # wait for a second to let the recognizer adjust the
    # energy threshold based on the surrounding noise level
    r.adjust_for_ambient_noise(source)
    print ("Say Something")
    # listens for the user's input
    audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print ("you said: " + text)
        if (text.lower().startswith("roku")):
            if (text.lower().endswith("left")):
                res = requests.post(url + "Left", data=payload, headers=headers)
            elif (text.lower().endswith("right")):
                res = requests.post(url + "Right", data=payload, headers=headers)
            elif (text.lower().endswith("select")):
                res = requests.post(url + "Select", data=payload, headers=headers)

            print(res)

    # error occurs when google could not understand what was said

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
