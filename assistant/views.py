from django.shortcuts import render

# Create your views here.
import os
import sys
import datetime
import time
import webbrowser
import json
import pickle
import numpy as np
import random
#import pyautogui
import pyttsx3
import speech_recognition as sr
import psutil
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from elevenlabs import generate, play
from .assistants import engine_talk, initialize_engine
from django.shortcuts import render
import comtypes
# other imports
import os


# rest of your code where you use pyautogui




#  Load API key
# from backend.api_key import api_key_data
# set_api_key(api_key_data)

# Load Model, Tokenizer, and Labels
MODEL_PATH = os.path.join(os.path.dirname(__file__), "backend/chat_model.h5")
TOKENIZER_PATH = os.path.join(os.path.dirname(__file__), "backend/tokenizer.pkl")
LABEL_ENCODER_PATH = os.path.join(os.path.dirname(__file__), "backend/label_encoder.pkl")
INTENTS_PATH = os.path.join(os.path.dirname(__file__), "backend/intents.json")

with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

# def initialize_engine():
#     comtypes.CoInitialize()
#     engine = pyttsx3.init("sapi5")
#     voices = engine.getProperty('voices')
#     engine.setProperty('voice', voices[1].id)
#     rate = engine.getProperty('rate')
#     engine.setProperty('rate', rate-50)
#     volume = engine.getProperty('volume')
#     engine.setProperty('volume', volume+0.25)
#     return engine
import pyttsx3
speak = pyttsx3.init()


  # Adjust speed (increase for faster speech)


def speak(text):
    comtypes.CoUninitialize()
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()
    engine.setProperty('rate', 180)
   
    
    
def finalize_engine():
    # Clean up COM resources after the operation
    comtypes.CoUninitialize()
def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening.......", end="", flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold=True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustment=2
        r.energy_threshold=4000
        r.phrase_time_limit = 10
        # print(sr.Microphone.list_microphone_names())
        audio = r.listen(source)
    try:
        print("\r" ,end="", flush=True)
        print("Recognizing......", end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print("\r" ,end="", flush=True)
        print(f"User said : {query}\n")
    except Exception as e:
        print("Say that again please")
        return "None"
    return query

def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
    return day_of_week

def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()

    if(hour>=0) and (hour<=12) and ('AM' in t):
        speak(f"Good morning Mishu, it's {day} and the time is {t}")
    elif(hour>=12)  and (hour<=16) and ('PM' in t):
        speak(f"Good afternoon Mishu, it's {day} and the time is {t}")
    else:
        speak(f"Good evening boss, it's {day} and the time is {t}")


def social_media(command):
    if 'facebook' in command:
        speak("opening your facebook")
        webbrowser.open("https://www.facebook.com/")
    elif 'whatsapp' in command:
        speak("opening your whatsapp")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'discord' in command:
        speak("opening your discord server")
        webbrowser.open("https://discord.com/")
    elif 'instagram' in command:
        speak("opening your instagram")
        webbrowser.open("https://www.instagram.com/")
    else:
        speak("No result found")



def schedule():
    day = cal_day().lower()
    speak("Boss today's schedule is ")
    week={
    "monday": "Boss, from 9:00 to 9:50 you have Algorithms class, from 10:00 to 11:50 you have System Design class, from 12:00 to 2:00 you have a break, and today you have Programming Lab from 2:00 onwards.",
    "tuesday": "Boss, from 9:00 to 9:50 you have Web Development class, from 10:00 to 10:50 you have a break, from 11:00 to 12:50 you have Database Systems class, from 1:00 to 2:00 you have a break, and today you have Open Source Projects lab from 2:00 onwards.",
    "wednesday": "Boss, today you have a full day of classes. From 9:00 to 10:50 you have Machine Learning class, from 11:00 to 11:50 you have Operating Systems class, from 12:00 to 12:50 you have Ethics in Technology class, from 1:00 to 2:00 you have a break, and today you have Software Engineering workshop from 2:00 onwards.",
    "thursday": "Boss, today you have a full day of classes. From 9:00 to 10:50 you have Computer Networks class, from 11:00 to 12:50 you have Cloud Computing class, from 1:00 to 2:00 you have a break, and today you have Cybersecurity lab from 2:00 onwards.",
    "friday": "Boss, today you have a full day of classes. From 9:00 to 9:50 you have Artificial Intelligence class, from 10:00 to 10:50 you have Advanced Programming class, from 11:00 to 12:50 you have UI/UX Design class, from 1:00 to 2:00 you have a break, and today you have Capstone Project work from 2:00 onwards.",
    "saturday": "Boss, today you have a more relaxed day. From 9:00 to 11:50 you have team meetings for your Capstone Project, from 12:00 to 12:50 you have Innovation and Entrepreneurship class, from 1:00 to 2:00 you have a break, and today you have extra time to work on personal development and coding practice from 2:00 onwards.",
    "sunday": "Boss, today is a holiday, but keep an eye on upcoming deadlines and use this time to catch up on any reading or project work."
    }
    if day in week.keys():
        speak(week[day]) 
def openApp(command):
    if "calculator" in command:
        speak("opening calculator")
        os.startfile('C:\\Windows\\System32\\calc.exe')
    elif "notepad" in command:
        speak("opening notepad")
        os.startfile('C:\\Windows\\System32\\notepad.exe')
    elif "paint" in command:
        speak("opening paint")
        os.startfile('C:\\Windows\\System32\\mspaint.exe')

def closeApp(command):
    if "calculator" in command:
        speak("closing calculator")
        os.system("taskkill /f /im calc.exe")
    elif "notepad" in command:
        speak("closing notepad")
        os.system('taskkill /f /im notepad.exe')
    elif "paint" in command:
        speak("closing paint")
        os.system('taskkill /f /im mspaint.exe')


def browsing(query):
    global state

    if 'google' in query:
        speak("Boss, what should I search on Google?")
        state = "google_search"
        s = command().lower()
        webbrowser.open(f"{s}")
    elif 'edge' in query:
        speak("Boss, what should i search on edge..")
        s = command().lower()
        webbrowser.open(f"{s}") 


def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Boss our system have {percentage} percentage battery")
    if percentage>=80:
        speak("Boss we could have enough charging to continue our recording")
    elif percentage>=40 and percentage<=75:
        speak("Boss we should connect our system to charging point to charge our battery")
    else:
        speak("Boss we have very low power, please connect to charging otherwise recording should be off...")

   
# if __name__ == "__main__":
def process_command(request):
  if request.method == 'POST':
    wishMe()
    while True:
        # query = request.POST.get('command', '').lower()
        # query  = input("Enter your command-> ")
        query = command().lower()
        if ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query):
            social_media(query)
        elif ("university time table" in query) or ("schedule" in query):
            schedule()
        #elif ("volume up" in query) or ("increase volume" in query):
            #pyautogui.press("volumeup")
            #speak("Volume increased")
        #elif ("volume down" in query) or ("decrease volume" in query):
            #pyautogui.press("volumedown")
            #speak("Volume decrease")
        #elif ("volume mute" in query) or ("mute the sound" in query):
            #pyautogui.press("volumemute")
            #speak("Volume muted")
        elif ("open calculator" in query) or ("open notepad" in query) or ("open paint" in query):
            openApp(query)
        elif ("close calculator" in query) or ("close notepad" in query) or ("close paint" in query):
            closeApp(query)
        elif ("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("thanks" in query) or ("hello" in query):
                padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
                result = model.predict(padded_sequences)
                tag = label_encoder.inverse_transform([np.argmax(result)])

                for i in data['intents']:
                    if i['tag'] == tag:
                        speak(np.random.choice(i['responses']))
        elif ("open google" in query) or ("open edge" in query):
            browsing(query)
        elif ("system condition" in query) or ("condition of the system" in query):
            speak("checking the system condition")
            condition()
        elif "exit" in query:
            sys.exit() 




# Load the model and tokenizer globally to avoid reloading it on every request.
