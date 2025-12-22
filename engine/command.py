import eel
import speech_recognition as sr
from engine.universal import handleDynamicQuery

@eel.expose
def toggle_listening():
    r = sr.Recognizer()

    try:
        eel.DisplayMessage("Listening...")
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.6)
            audio = r.listen(source, timeout=8, phrase_time_limit=7)

        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language="en-IN").lower()

        eel.DisplayMessage(f"You said: {query}")
        handleDynamicQuery(query)

    except sr.WaitTimeoutError:
        eel.DisplayMessage("No speech detected")

    except sr.UnknownValueError:
        eel.DisplayMessage("Sorry, I couldn’t understand")

    except Exception as e:
        eel.DisplayMessage("Microphone error")
        print(f"[MIC ERROR] {e}")
