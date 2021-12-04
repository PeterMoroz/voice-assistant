import speech_recognition as sr
import pyttsx3
import requests
import datetime
import wikipedia

from configparser import ConfigParser

recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 120)

config = ConfigParser()
config.read('voice-assistant.ini')


def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def greet_me():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 6:
        speak('Good night master !')
    elif hour >= 6 and hour < 12:
        speak('Good morning master !')
    elif hour >= 12 and hour < 18:
        speak('Good afternoon master !')
    else:
        speak('Good evening master !')

def listen():
    try:
        with sr.Microphone(device_index=0) as mic:
            recognizer.adjust_for_ambient_noise(mic)
            print('listening ...')
            recognizer.pause_threshold = 0.7
            voice = recognizer.listen(mic)
            print('recognizing ...')
            text = recognizer.recognize_google(voice)
            text = text.lower()
            print(f"user said: {text}\n")
    except sr.UnknownValueError:
        print('Google speech recognition could not understand audio')
        return ''
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; " + str(e))
        return None
    except Exception as e:
        print("Exception: " + str(e))
        return None
    return text
    
def get_the_weather_sentence(r):
    T0 = 273.15
    print('weather response:\n' + str(r))
    if r['cod'] == 200:
       m = r['main']
       t = m['temp']
       p = m['pressure']
       h = m['humidity']
       w = r['weather']
       d = w[0]['description']
       text = 'Today is ' + str(d)
       text += ' the temperature is ' + '{0:.2f}'.format(t - T0) + ' celsius degrees, the pressure is ' + str(p) + ' hectopascals, the humidity is ' + str(h) + ' percentage '
    elif r['cod'] == 404:
       text = 'The city not found!'
    else:
       text = 'The weather service is unavailable. Repeat later please.'        
    return text
        
def run_assistant():
    cmd = listen()    
    if cmd == None:
        return
    if cmd == '':
        speak("I'm sorry, I didn't catch that.")
        return
    if 'time' in cmd:
        time = datetime.datetime.now().strftime('%H: %M: %S')
        print(f"current time is: {time}\n")
        speak('current time is ' + time)
    elif 'tell me about' in cmd:
        speak('Searching the wikipedia, please wait.')
        thing = cmd.replace('tell me about', '')
        info = wikipedia.summary(thing, 3)
        print(f"The Wikipedia tells about {thing}:\n")
        print(info)
        speak(info)
    elif 'search' in cmd:
        speak('Searching the wikipedia, please wait.')
        thing = cmd.replace('search', '')
        info = wikipedia.summary(thing, 3)
        print(f"The Wikipedia tells about {thing}:\n")
        print(info)
        speak(info)
    elif 'who are you' in cmd:
        speak('I am your personal assistant')
    elif 'weather' in cmd:
        speak('what is the city interested you ?')
        city = listen()
        repeat_count = 0
        while city == '' and repeat_count < 4:
            speak("I'm sorry, I didn't catch.")
            city = listen()
            repeat_count += 1
        if city == None:
            return
        if city == '':
            speak("I'm sorry, I don't understand you.")
            return

        BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
        app_id = config.get('openweather', 'app_id')
        speak('Requesting the weather, please wait.')
        url = BASE_URL + '?appid=' + app_id + '&q=' + city
        response = requests.get(url)
        r = response.json()
        text = get_the_weather_sentence(r)
        if text != None:
            print(text)
            speak(text)
        else:
            print('Could not get the weather sentence')
    else:
        speak("I'm sorry, I'm not sure I follow you.")

if __name__ == '__main__':
    greet_me()
    while True:
        run_assistant()