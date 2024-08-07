from openai import OpenAI
import os
import speech_recognition as sr
import pyttsx3
import sys

# OpenAI API key
client = OpenAI(api_key="<API-key>")

# Text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('volume',0.2)
r=sr.Recognizer()

def listen_and_respond():
    # Listen for input
    with sr.Microphone(device_index=1) as source:
        while True:
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = r.listen(source, phrase_time_limit = 5, timeout = 10)
            print("Audio Recorded")
            
            try:
                prompt = r.recognize_google(audio, language="en-EN", show_all=False)
                print("You asked:", prompt)
                response = client.completions.create(model = "gpt-3.5-turbo-instruct", prompt = prompt, max_tokens = 300, temperature = 0.7)
                # Get the response text
                response_text = response.choices[0].text
                print(response_text)

                # Speak the response
                engine.say(response_text)
                engine.runAndWait()
                print()
            
            
            # Catch if recognition fails
            except sr.UnknownValueError:
                response_text = "Sorry, I didn't understand what you said"
                print(response_text)
                engine.say(response_text)
                engine.runAndWait()
                print()
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))



def main():
    while True:
        listen_and_respond()

if __name__ == "__main__":
    main()
