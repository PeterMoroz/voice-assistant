import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia

recognizer = sr.Recognizer()
engine = pyttsx3.init()



def talk(text):
    engine.say(text)
    engine.runAndWait()
    
def greet_me():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 6:
        talk('Good night master !')
    elif hour >= 6 and hour < 12:
        talk('Good morning master !')
    elif hour >= 12 and hour < 18:
        talk('Good afternoon master !')
    else:
        talk('Good evening master !')

def take_command():
    try:
        with sr.Microphone(device_index=0) as mic:
            recognizer.adjust_for_ambient_noise(mic)
            print('listening ...')
            voice = recognizer.listen(mic)
            print('recognizing ...')
            text = recognizer.recognize_google(voice)
            text = text.lower()
            print(f"user said: {text}\n")
    except sr.UnknownValueError:
        print('Google speech recognition could not understand audio')
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; " + str(e))
    except Exception as e:
        print("Exception: " + str(e))
        return None
    return text
        
def run_assistant():
    cmd = take_command()    
    if 'time' in cmd:
        # time = datetime.datetime.now().strftime('%I: %M')
        time = datetime.datetime.now().strftime('%H: %M: %S')
        print(f"current time is: {time}\n")
        talk('current time is ' + time)
    elif 'tell me about' in cmd:
        thing = cmd.replace('tell me about', '')
        info = wikipedia.summary(thing, 3)
        print(f"The Wikipedia tells about {thing}:\n")
        print(info)
        talk(info)
    elif 'who are you' in cmd:
        talk('I am your personal assistant')
    elif 'what can you do for me' in cmd:
        talk('I can tell time and help you go with wikipedia')
    else:
        talk('I did not understand, please repeat again')

if __name__ == '__main__':
    greet_me()
    while True:
        run_assistant()