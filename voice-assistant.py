import speech_recognition as sr
import pyttsx3
import requests
import datetime
import wikipedia
import urllib.parse

from pprint import pprint

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
    
def wiki_search(q=''):
    speak('Searching the wikipedia, please wait.')
    info = wikipedia.summary(q)
    print(f"The Wikipedia tells about {q}:\n{info}")
    speak(info)

def wolfram_alpha_query(q=''):
    app_id = config.get('wolframalpha', 'app_id')
    query = urllib.parse.quote_plus(q)
    query_url = f"http://api.wolframalpha.com/v2/query?" \
                f"appid={app_id}" \
                f"&input={query}" \
                f"&format=plaintext" \
                f"&output=json"

    response = requests.get(query_url)
    if response == None:
        print(f"No response to '{q}'\n")
        # speak('No response from knowledges base')
        return
    
    r = response.json().get('queryresult', {})
    print('response:\n' + str(r))
    if r['error']:
    	print('Error in response')
    	return

    if not r['success']:
    	print('Could not get answer')
    	return

    pod0 = r['pods'][0]
    pod1 = r['pods'][1]
    title = pod1.get('title', '').lower()
    if ('definition' in title or 'result' in title or (pod1.get('primary', False))):
        subpod = pod1['subpods'][0]
        if isinstance(subpod, list):
            answer = subpod[0].get('plaintext', '')
        else:
            answer = subpod.get('plaintext', '')
        print(f"answer to '{q} is:\n{answer}")

    else:
        subpod = pod0['subpods'][0]
        if isinstance(subpod, list):
            question = subpod[0].get('plaintext', '')
        else:
            question = subpod.get('plaintext', '')
        print(f"ask wikipedia about: '{question}'")
        q = question.split('(')[0]
        wiki_search(q)
        
def wolfram_alpha_solve(q=''):
    app_id = config.get('wolframalpha', 'app_id')
    query = urllib.parse.quote_plus(q)
    query = urllib.parse.quote_plus(q)
    query_url = f"http://api.wolframalpha.com/v2/query?" \
                f"appid={app_id}" \
                f"&input={query}" \
                f"&includepodid=Result" \
                f"&output=json"
                
    response = requests.get(query_url)
    if response == None:
        print(f"No response to '{q}'\n")
        # speak('No response from solver')
        return
    
    r = response.json().get('queryresult', {})
    print('response:\n' + str(r))
    if r['success'] and not r['error']:
        pod0 = r['pods'][0]
        if ((pod0.get('title', '').lower() == 'result') and (pod0.get('numsubpods', 0) > 0) and not (pod0.get('error', False))):
            subpods = pod0['subpods'] 
            answer = subpods[0].get('plaintext', '')
            print(f"answer to '{q}' is {answer}\n")
        else:
            print(f"Could not solve '{q}'\n")
            # speak('Could not solve.')
    
def wolfram_alpha_ask(q=''):
    app_id = config.get('wolframalpha', 'app_id')
    query_url = f"http://api.wolframalpha.com/v1/spoken?appid={app_id}&i={q}"
    response = requests.get(query_url)
    if response != None:
        text = response.text
        print(f"answer to '{q}' is:\n{text}")
        speak(text)
    else:
        print('No response')
        speak('No response')
        
# def wolfram_alpha_conversation():
    
        
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
            speak('Could not get the weather, try later please.')
            
    elif cmd.startswith('tell me about'):
        # when command begins from 'tell me about' query the WolframAlpha and fallback to Wikipedia if failed
        thing = cmd.replace('tell me about', '')    
        wolfram_alpha_query(thing)
    elif cmd.startswith('search'):
        # when command begins from 'search' ask the Wikipedia
        thing = cmd.replace('search', '')
        wiki_search(thing)
    elif cmd.startswith('solve'):
        wolfram_alpha_solve(cmd)
    elif cmd.startswith('who') or cmd.startswith('what') or cmd.startswith('where') or cmd.startswith('when') or cmd.startswith('why') or cmd.startswith('which') or cmd.startswith('how'):
        wolfram_alpha_ask(cmd)
    elif 'start conversation' in cmd or 'begin conversation' in cmd:
        wolfram_alpha_conversation()
    else:
        speak("I'm sorry, I'm not sure I follow you.")

if __name__ == '__main__':
    greet_me()
    while True:
        run_assistant()