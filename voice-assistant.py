import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone(device_index=0) as mic:
            recognizer.adjust_for_ambient_noise(mic)
            print("say something")
            voice = recognizer.listen(mic)
            instruct = recognizer.recognize_google(voice)
            instruct = instruct.lower()
            print(instruct)
            return instruct
    except Exception as ex:
        print("Exception: " + str(ex))
        return None
        
def run_assistant():
    instruct = take_command()    
    if 'time' in instruct:
        time = datetime.datetime.now().strftime('%I: %M')
        print(time)
        talk('current time is ' + time)
    elif 'tell me about' in instruct:
        thing = instruct.replace('tell me about', '')
        info = wikipedia.summary(thing, 2)
        print(info)
        talk(info)
    elif 'who are you' in instruct:
        talk('I am your personal assistant')
    elif 'what can you do for me' in instruct:
        talk('I can tell time and help you go with wikipedia')
    else:
        talk('I did no understand, please repeat again')

while True:
    run_assistant()