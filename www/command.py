import time
import pyttsx3
import speech_recognition as sr
import eel
import pyjokes
import requests,json
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    #print(voices)
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 170)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()

@eel.expose
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=6)
    
    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='en')
        print(f'User said: {query}')
        #speak(query)
        time.sleep(2)
        eel.DisplayMessage(query)
        
        

    except Exception as e:
        return ""
    
    return query.lower()

# text = takeCommand()

# speak(text)
@eel.expose
def allCommands():
    query = takeCommand()
    print(query)

    # Pre-requisite responses
    if any(greet in query for greet in ['hi', 'hello', 'hey']):
        speak("Hello! How can I assist you today?")
        eel.ShowHood()
        return

    elif "joke" in query:
        speak(pyjokes.get_joke())
        eel.ShowHood()
        return

    elif "weather" in query:
        api_key = "434e4eda7184472a883d3bc41ff902d8" # Replace with your actual OpenWeatherMap API key
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = query.split("in")[-1].strip()
        complete_url = base_url + "q=" + city_name + "&appid=" + api_key

        response = requests.get(complete_url)
        weather_data = response.json()

        if weather_data["cod"] != "404":
            main = weather_data["main"]
            wind = weather_data["wind"]
            weather_description = weather_data["weather"][0]["description"]

            speak(f"Weather in {city_name}: {weather_description}.")
            eel.ShowHood()
            return
        else:
            speak("City not found.")
            eel.ShowHood()
            return

    if 'open' in query:
        from engine.features import openCommand
        openCommand(query)

    elif 'on youtube' in query:
        from engine.features import PlayYoutube
        PlayYoutube(query)
    else:
        print('Not run')

    eel.ShowHood()

