import pyttsx3
from requests.api import get
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
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jarvis_ui import Ui_jarvis

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

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
    main_url = "http://newsapi.org/v2/top-headlines?sources=techchurch&apIKey=380917c7d8a54945b11eeddde39d0168"
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

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()
    def run(self):
        self.start()
    def takeCommand(self):
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

    def start(self):
        wish()
        while True:
        #if 1:
            self.query = self.takeCommand().lower()
            if "open notepad" in self.query:
                npath = "C:\\Windows\\system32\\notepad.exe"
                os.startfile(npath)
            elif "open command prompt" in self.query:
                os.system("start cmd")
            elif "open camera" in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow("webcam",img)
                    k = cv2.waitKey(50)
                    if k==27:
                        break
                cap.release()
                cv2.destroyAllWindows()
            elif "wikipedia" in self.query:
                speak("Searching wikipedia....")
                self.query = self.query.replace("wikipedia","")
                results = wikipedia.summary(self.query, sentences=2)
                speak("According to wikipedia")
                speak(results)
            elif "open youtube" in self.query:
                webbrowser.open("www.youtube.com")
            elif "open google" in self.query:
                speak("Sir what should i search on google")
                cm = self.takeCommand().lower()
                webbrowser.open(f"{cm}")
            elif "send a message" in self.query:
                speak("What should i deliver")
                cm = self.takeCommand().lower()
                kit.sendwhatmsg("+919958203031",f"{cm}",2,25)
            elif "no thanks" in self.query:
                speak("I hope you have a good day sir. Bye")
                sys.exit()
            elif "close notepad" in self.query:
                speak("okay sir, closing notepad")
                os.system("taskkill /f /im notepad.exe")
            elif "joke" in self.query:
                joke = pyjokes.get_joke()
                speak(joke)
            elif "shut down the system" in self.query:
                os.system("shutdown /s /t 5")
            elif "restart the sytem" in self.query:
                os.system("restart /r /t 5")
            elif "sleep the system" in self.query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            elif "switch the window" in self.query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")
            elif "news" in self.query:
                speak("Please wait, fetching news...")
                news()
            elif "where am i" in self.query or "where are we" in self.query:
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
            elif "instagram profile" or "profile on instagram" in self.query:
                speak("sir please enter the user name correctly")
                name = input("Enter the username :")
                webbrowser.open(f"www.instagram.com/{name}")
                speak("Sir here is the profile")
                time.sleep(5)
                speak("Sir would you like to download the profile pic of this account")
                cn = self.takeCommand().lower()
                if "yes" in cn:
                    mod = instaloader.Instaloader()
                    mod.download_profile(name, profile_pic_only=True)
                    speak("I am done sir, profile picture is saved in our main folder")
                else:
                    pass
            
            elif "take screenshot" in self.query or "take a screenshot" in self.query:
                speak("Sir what should i name the file")
                name = self.takeCommand().lower()
                speak("Taking screenshot...")
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("Screenshot taken")

            elif "read pdf" in self.query:
                pdf_reader()

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_jarvis()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)
    
    def startTask(self):
        self.ui.movie = QtGui.QMovie("jarvis.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie = QtGui.QMovie("start.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString("hh mm ss")
        label_date = current_date.toString("Qt.ISODate")
        self.ui.textBrowser.setText(label_time)
        self.ui.textBrowser_2.setText(label_date)

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())