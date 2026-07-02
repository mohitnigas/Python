import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import music_library
from openai import OpenAI
import pygame
import importlib

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    try:
        gtts = importlib.import_module('gtts')
        tts = gtts.gTTS(text)
        tts.save('temp.mp3')

        # Initialize Pygame mixer
        pygame.mixer.init()

        # Load the MP3 file
        pygame.mixer.music.load('temp.mp3')

        # Play the MP3 file
        pygame.mixer.music.play()

        # Keep the program running until the music stops playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        os.remove("temp.mp3")
    except ModuleNotFoundError:
        engine.say(text)
        engine.runAndWait()


def ai_process_command(command):
    # Use OpenAI API to process the command
    client = OpenAI(api_key="<Your Key Here>",
    )


    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short respones to the user."},
    {"role": "user", "content": command}
  ]
)      
    return completion.choices[0].message.content.strip()


if __name__ == "__main__":
    speak("INITIALIZING VOICE ASSISTANT")
    while True:
        # listen for user input
        # obtain audio from the microphone
        with sr.Microphone() as source:
            print("listening...")
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)

            print("recognizing...")

        # recognize speech using Google Speech Recognition
            try:
                command = recognizer.recognize_google(audio)
                print(f"You said: {command}")

                # process the command
                if "open Google" in command:
                    speak("Opening Google")
                    webbrowser.open("https://www.google.com")
                elif "open YouTube" in command:
                    speak("Opening YouTube")
                    webbrowser.open("https://www.youtube.com")
                elif "open Facebook" in command:
                    speak("Opening Facebook")
                    webbrowser.open("https://www.facebook.com")
                elif "open Twitter" in command:
                    speak("Opening Twitter")
                    webbrowser.open("https://www.twitter.com")
                elif "open Instagram" in command:
                    speak("Opening Instagram")
                    webbrowser.open("https://www.instagram.com")
                elif "open LinkedIn" in command:
                    speak("Opening LinkedIn")
                    webbrowser.open("https://www.linkedin.com")
                elif "play music" in command:
                    speak("Playing music")
                    # play a random song from the music library
                    import random
                    song = random.choice(list(music_library.music.keys()))
                    url = music_library.music[song]
                    speak(f"Playing {song}")
                    webbrowser.open(url)
                elif "exit" in command:
                    speak("Exiting the voice assistant. Goodbye!")
                    break
                else:
                   #let openAI handle the command
                   output =  ai_process_command(command)
                   speak(output)

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")