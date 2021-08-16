import datetime
import winsound
import pyttsx3

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def alarm(Timing):
    altime = str(datetime.datetime.now().strptime(Timing,"%I:%M %p"))
    altime = altime[11:-3]
    Horeal = altime[:2]
    Horeal = int(Horeal)
    Mireal = altime[3:5]
    Mireal = int(Mireal)
    speak(f"Done, alarm is set for {Timing}")

    while True:
        if Horeal == datetime.datetime.now().hour:
            if Mireal == datetime.datetime.now().minute:
                print("Alarm is running")
                winsound.PlaySound('abc',winsound.SND_LOOP)

            elif Mireal < datetime.datetime.now().minute:
                break
    
if __name__ == '__main__':
    alarm('8:00 AM')
