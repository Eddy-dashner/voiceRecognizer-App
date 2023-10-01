import os
import time
import pyaudio
import speech_recognition as sr
import pygame  # Import pygame instead of playsound
from gtts import gTTS
import openai
from dotenv import load_dotenv

api_key = os.getenv("API_KEY")

lang = 'en'

openai.api_key = api_key

guy = ""

while True:
    def get_adio():
        r = sr.Recognizer()
        with sr.Microphone(device_index=1) as source:
            audio = r.listen(source)
            said = ""

            try:
                said = r.recognize_google(audio)
                print(said)
                global guy
                guy = said

                if "siri" in said:
                    words = said.split()
                    new_string = ' '.join(words[1:])
                    print(new_string)
                    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": said}])
                    text = completion.choices[0].message.content
                    speech = gTTS(text=text, lang=lang, slow=False, tld="com.au")
                    speech.save("welcome1.mp3")
                    pygame.mixer.init()  
                    pygame.mixer.music.load("welcome1.mp3")
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)

            except Exception:
                print("Exception")

        return said

    if "stop" in guy:
        break

    get_adio()
