import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import wikipedia
import webbrowser
import pywhatkit as kit
import sys
import pyjokes
import pyautogui
import time
import requests
import instaloader
import PyPDF2
import json
from bs4 import BeautifulSoup
from pywikihow import search_wikihow

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()



def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning")
    elif hour>=12 and hour<=18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Jarvis. Sir please tell me how may I help you")
def news():
    main_url = 'https://newsapi.org/v2/top-headlines?country = in&apIKey=380917c7d8a54945b11eeddde39d0168'
    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    days = ["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(days)):
        speak(f"today's {days[i]} news is: {head[i]}")

def pdf_reader():
    book = open("D:\\Jayesh\\jee\\physics\\Concepts of Physics Part 2 by HC Verma.pdf")
    pdfReader = PyPDF2.PdffileReader(book)
    pages = pdfReader.numPages
    speak(f"Total numbers of pages in this book {pages}")
    speak("what page should i read. Please enter the page number")
    pg = int(input("Enter the page number: "))
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
    try:
        print("Recognising...")
        query = r.recognize_google(audio,language="en-in")
        print(f"user said :{query}")
    except Exception as e:
        speak("say again")
        return "none"
    return query

def temp():
    speak("At what location")
    cm = takeCommand().lower()
    url = f"https://www.google.com/search?q={cm}"
    r = requests.get(url)
    data = BeautifulSoup(r.text,"html.parser")
    temp = data.find("div",class_="BNeawe").text
    speak(f"the temperature in {cm} is {temp}")

def play():
    speak("What song should i play")
    cm = takeCommand().lower()
    kit.playonyt(f'{cm}')

def start():
    wish()
    while True:
    #if 1:
        query = takeCommand().lower()
        if "open notepad" in query:
            npath = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(npath)
        elif "open command prompt" in query:
            os.system("start cmd")
        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow("webcam",img)
                k = cv2.waitKey(50)
                if k==27:
                    break
            cap.release()
            cv2.destroyAllWindows()
        elif "wikipedia" in query:
            speak("Searching wikipedia....")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            speak(results)
        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")
        elif "open google" in query:
            speak("Sir what should i search on google")
            cm = takeCommand().lower()
            webbrowser.open(f"{cm}")
        elif "send a message" in query:
            speak("What should i deliver")
            cm = takeCommand().lower()
            kit.sendwhatmsg("+919958203031",f"{cm}",2,25)
        elif "sleep" in query:
            speak("I hope you have a good day sir. Bye")
            per()
        elif "close notepad" in query:
            speak("okay sir, closing notepad")
            os.system("taskkill /f /im notepad.exe")
        elif "joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)
        elif "shut down the system" in query:
            os.system("shutdown /s /t 5")
        elif "restart the sytem" in query:
            os.system("restart /r /t 5")
        elif "sleep the system" in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif "switch the window" in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")
        elif "news" in query:
            speak("Please wait, fetching news...")
            news()
        elif "where am i" in query or "where are we" in query:
            speak("wait sir, let me check")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                url = 'https://get.geojs.io/v1/ip/geo'+ipAdd+'.json'
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()
                city = geo_data['city']
                country = geo_data['country']
                speak(f"sir i am not sure, but i think we are in {city} in country {country}")
            except Exception as e:
                speak("sorry sir not able to find out")
                pass
        elif "activate how to mod" in query:
            speak("how to mode is activate")
            while True:
                speak("please tell me what do you want to know")
                how = takeCommand().lower()
                try:
                    if "exit" in how or "close" in how:
                        speak("okay sir how to mode is closed")
                        break
                    else:
                        max_results = 1
                        how_to = search_wikihow(how, max_results)
                        assert len(how_to) == 1
                        how_to[0].print()
                        speak(how_to[0].summary)
                except Exception as e:
                    speak("Sorry sir i am not able to find it")
        elif "send sms" in query:
            speak("What should is say")
            ms = takeCommand().lower()
            from twilio.rest import Client
            account_sid = "ACede96d6bba0bddb0d21db89bb77702d8"
            auth_token = "0343b91eceee965234d2d18f1b3ebcb0"
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                     body=f'{ms}',
                     from_='+14243961253',
                     to='+918178120249'
                 )

            print(message.sid)
        elif 'alarm' in query:
            speak("Sir please tell the time to set the alarm")
            tt = takeCommand().lower()
            tt = tt.replace("set alarm to","")
            tt = tt.replace(".","")
            tt = tt.upper()
            import MyAlarm
            MyAlarm.alarm(tt)
        elif "take screenshot" in query or "take a screenshot" in query:
            speak("Sir what should i name the file")
            name = takeCommand().lower()
            speak("Taking screenshot...")
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("Screenshot taken")
        elif "read pdf" in query:
            pdf_reader()
        elif "temperature" in query:
            temp()
        elif "play a song" in query:
            play()
            per()
        
def per():
    permission = takeCommand().lower()
    if "wake up" in permission or "hey" in permission:
        start()
    elif "goodbye" in permission:
        speak("Thanks for using me sir")
        sys.exit()

if __name__=="__main__":
    while True:
        per()
