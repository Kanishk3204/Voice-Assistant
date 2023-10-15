import speech_recognition as sr
import os
import pyttsx3
import webbrowser
import wikipedia
import pyjokes
import pywhatkit as pw
import datetime

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def say(sentence):
    engine.say(sentence)
    engine.runAndWait()


def greet():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        print("Good Morning !")
        say("Good Morning !")
    elif 12 <= hour < 16:
        print("Good afternoon ! ")
        say("Good afternoon ! ")
        engine.runAndWait()
    else:
        print("Good evening  !")
        say("Good evening  !")
    print("I am Kash, Your personal voice assistant, what can i do for you?")
    say("I am Kash, Your personal voice assistant, what can i do for you?")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold =  0.8
        audio=r.listen(source)
        try:
            print('recognising...')
            query = r.recognize_google(audio,language="en-in")
            print(f"You said:{query}")
            return query.lower()
        except:
            return "Sorry!! Something went wrong"

cond = True
def action():
    global cond
    while True:
        query = takecommand()
        sites = [["youtube", "https://youtube.com"], ["facebook", "https://facebook.com"],
                 ["google", "https://google.com"], ["twitter", "https://twitter.com"],
                 ["word", "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word"],
                 ["powerpoint", "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint"],
                 ["brave browser", "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Brave"]]
        for site in sites:
            if f"open {site[0]}" in query.lower():
                say(f"opening {site[0]}")
                webbrowser.open(site[1])
        if 'stop' in query:
            print('ok,I will talk to you later, Goodbye!!!')
            say('ok,I will talk to you later, Goodbye!!!')
            cond=False
            break
        if "play on youtube" in query:
            video = query.replace('play on youtube', '')
            say("playing" + video)
            pw.playonyt(video)
        elif "search" in query:
            what = query.replace('search', '')
            say(f"searching {what}")
            pw.search(what)
        elif "hello cash" in query:
            print("Hello Kanishk what can I do for You?")
            say("Hello Kanishk what can I do for You?")
        elif "what is your name" in query:
            print("my name is Kash")
            say("My name is Kash")
        elif 'who is' in query:
            person = query.replace('who is', '')
            info = wikipedia.summary(person, 1)
            print(info)
            say(info)
        elif 'what is' in query:
            person = query.replace('what is', '')
            info = wikipedia.summary(person, 1)
            print(info)
            say(info)
        elif 'joke' in query:
            joke = pyjokes.get_joke()
            print(joke)
            say(joke)
        elif 'open music' in query:
            musicpath = "D:\downloads new\Lord.Huron-The.Night.We.Met.mp3"
            os.startfile(musicpath)
        elif 'time' in query:
            time = datetime.datetime.now().strftime('%I:%M:%S %p')
            hour = datetime.datetime.now().strftime('%I:%M %p')
            print(f"time is {time}")
            say(f"time is {hour}")
        elif 'camera' in query:
            os.startfile("microsoft.windows.camera:")
        elif 'send message on whatsapp' in query:
            say('enter phone number')
            phone=input('phone number:- ')
            say('enter message')
            message=input('message:- ')
            pw.sendwhatmsg(phone,message,datetime.datetime.now().hour,datetime.datetime.now().minute+1)

greet()

while cond:
    action()
