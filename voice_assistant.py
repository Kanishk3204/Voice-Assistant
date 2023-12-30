import speech_recognition as sr
import os
import pyttsx3
import webbrowser
import wikipedia
import pyjokes
import pywhatkit as pw
import datetime
import pandas as pd
import ast
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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


def verify_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        say("Please tell me the key before we get started")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

        try:
            key = recognizer.recognize_google(audio).lower()
            print(f"You said:- {key}")
            if key == "hey cash it's kanishk" or key == "hey cash its kanishk":
                say("Verification successful.")
                return True
            else:
                say("Sorry, I couldn't verify your voice.")
                return False
        except sr.UnknownValueError:
            say("Sorry, I couldn't understand your voice.")
            return False
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return False

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
            return query
        except:
            return "Sorry!! Something went wrong"


def movie(command):
    movies = pd.read_csv('data/tmdb_5000_movies.csv')
    credits = pd.read_csv('data/tmdb_5000_credits.csv')
    movies = movies.merge(credits,on='title')
    movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
    def convert(text):
        L = []
        for i in ast.literal_eval(text):
            L.append(i['name'])
        return L
    movies.dropna(inplace=True)
    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)

    ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')
    movies['cast'] = movies['cast'].apply(convert)
    movies['cast'] = movies['cast'].apply(lambda x:x[0:3])
    def fetch_director(text):
        L = []
        for i in ast.literal_eval(text):
            if i['job'] == 'Director':
                L.append(i['name'])
        return L
    movies['crew'] = movies['crew'].apply(fetch_director)
    def collapse(L):
        L1 = []
        for i in L:
            L1.append(i.replace(" ",""))
        return L1
    movies['cast'] = movies['cast'].apply(collapse)
    movies['crew'] = movies['crew'].apply(collapse)
    movies['genres'] = movies['genres'].apply(collapse)
    movies['keywords'] = movies['keywords'].apply(collapse)
    movies['overview'] = movies['overview'].apply(lambda x:x.split())
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    new = movies.drop(columns=['overview','genres','keywords','cast','crew'])
    new['tags'] = new['tags'].apply(lambda x: " ".join(x))

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(new['tags']).toarray()

    similarity = cosine_similarity(vector)
    similarity
    new[new['title'] == 'The Lego Movie'].index[0]
    listofmovies = []

    def recommend(movie):
        index = new[new['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        for i in distances[1:6]:
            listofmovies.append(new.iloc[i[0]].title)

    recommend(command)
    return listofmovies


#function for sentiment analysis
def sentiment(query):
    analyser = SentimentIntensityAnalyzer()
    v = analyser.polarity_scores(query)
    if(v['neg'] > v['neu'] and v['neg'] > v['pos']):
        say("I'm sorry to hear that you're feeling down. Is there anything I can do to help or brighten your day?")
        say("For example I can tell you a joke or can suggest you movies to watch.")
        print("I'm sorry to hear that you're feeling down. Is there anything I can do to help or brighten your day?")
        print("For example I can tell you a joke or can suggest you movies to watch.")
    elif(v['pos'] > v['neg'] and v['pos'] > v['neu']):
        say("That's great to hear! I'm here to make your day even better.")
        print("That's great to hear! I'm here to make your day even better.")
    else:
        say("I sense a neutral sentiment. How can I assist you today?")
        print("I sense a neutral sentiment. How can I assist you today?")



# function to take actions according to the query
def action():
    global cond
    while True:
        query = takecommand()
        query = query.lower()
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
        elif "recommend" in query:
            say("what's the last one you watched")
            print("what's the last one you watched")
            filmname = takecommand()
            suggested = movie(filmname)
            say("These are the movies you can watch")
            for i in range (5):
                say(suggested[i])
                print(suggested[i])
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
        else:
            sentiment(query)

#main program
cond = verify_user()
if cond:
    greet()

while cond:
    action()
