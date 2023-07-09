import speech_recognition as sr
import os
import pyttsx3
import webbrowser
import wikipedia
import pyjokes
import pywhatkit as pw
import datetime
import subprocess

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice' , voices[1].id)

def say(sentence):
    engine.say(sentence)
    engine.runAndWait()

def takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold =  0.6
        audio=r.listen(source)
        try:
            print('recognising...')
            query = r.recognize_google(audio,language="en-in")
            print(f"user said:{query}")
            return query.lower()
        except:
            return "Sorry!! Something went wrong"

def action():
    query=takecommand()
    sites=[["youtube","https://youtube.com"],["wikipedia","https://wikipedia.com"],["google","https://google.com"]]
    for site in sites:
        if f"open {site[0]}" in query.lower():
            say(f"opening {site[0]}")
            webbrowser.open(site[1])
    if 'open music' in query:
        musicpath= "D:\downloads new\Lord.Huron-The.Night.We.Met.mp3"
        os.startfile(musicpath)
    if 'time' in query:
        time = datetime.datetime.now().strftime('%I:%M:%S %p')
        hour = datetime.datetime.now().strftime('%I:%M %p')
        print(f"time is {time}")
        say(f"time is {hour}")
    # elif "camera" in query or "take a photo" in query:
    #     ec.capture(0, "Jarvis Camera ", "img.jpg")
    if 'camera' in query:
        os.startfile("microsoft.windows.camera:")
    if 'calculator' in query:
        os.startfile("microsoft.windows.calculator:")
    if 'send message at night to kashish' in query:
        # say('please enter the contact')
        # contact = input("Enter the name of the contact: ")
        # message = input("Enter the message: ")
        pw.sendwhatmsg('+91 84481 79695','raat ko message through voice assistant',5,30,10000)
    # if 'send message' in query:
    #     say('please enter the contact')
    #     contact = input("Enter the name of the contact: ")
    #     message = input("Enter the message: ")
    #     pw.sendwhatmsg(contact, message, datetime.datetime.now().hour, datetime.datetime.now().minute + 1)

action()