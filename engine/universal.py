import os
import re
import sys
import time
import threading
import webbrowser
import subprocess
import shutil
import pywhatkit
import eel
import google.generativeai as genai
from datetime import datetime
from engine.speech import is_speaking,speak, stopSpeaking
from engine.config import ASSISTANT_NAME

# ================== GEMINI CONFIG ==================
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

conversation_history = []
MAX_HISTORY = 6

# ================== TIME-BASED GREETING ==================
def get_time_based_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 15:
        return "Good afternoon"
    elif 15 <= hour:
        return "Good evening"
    
# ================== DYNAMIC WINDOWS APP SEARCH ==================
def openWindowsAppDynamic(app_name):
    """
    Dynamically finds and opens any Windows app (UWP or classic)
    """
    try:
        ps_command = f'''
        Get-StartApps |
        Where-Object {{$_.Name -like "*{app_name}*"}} |
        Select-Object -First 1 -ExpandProperty AppID
        '''

        result = subprocess.check_output(
            ["powershell", "-Command", ps_command],
            text=True
        ).strip()

        if result:
            subprocess.Popen(
                f'explorer.exe shell:AppsFolder\\{result}',
                shell=True
            )
            return True

        return False

    except Exception as e:
        print(f"[WINDOWS APP SEARCH ERROR] {e}")
        return False

# ================== OPEN APPS / WEBSITES ==================
def openAppOrWebsite(query):
    query = query.replace("open", "").replace(ASSISTANT_NAME.lower(), "").strip().lower()
    speak(f"Opening {query}")

    try:
        # Websites
        if "." in query or "www" in query or "com" in query:
            if not query.startswith("http"):
                query = "https://" + query
            webbrowser.open(query)
            return

        # 🔥 Dynamic Windows app open (UWP + classic)
        if openWindowsAppDynamic(query):
            return

        # Fallback: executable in PATH
        app_path = shutil.which(query)
        if app_path:
            subprocess.Popen(app_path)
            return

        # Final fallback: Google search
        speak(f"I couldn't find {query}. Searching online.")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    except Exception as e:
        speak("Sorry, I couldn't open that.")
        print(f"[OPEN ERROR] {e}")

# ================== GOOGLE SEARCH ==================
def searchWeb(query):
    term = re.sub(r"(search|find|look up|google)", "", query, flags=re.IGNORECASE).strip()
    if not term:
        speak("Please tell me what to search for.")
        return

    speak(f"Searching Google for {term}")
    url = f"https://www.google.com/search?q={term}"

    try:
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))
        webbrowser.get("chrome").open(url)
    except:
        webbrowser.open(url)

# ================== YOUTUBE ==================
def playYouTube(query):
    song = query.replace("play", "").replace("on youtube", "").strip()
    speak(f"Playing {song} on YouTube")
    pywhatkit.playonyt(song)

# ================== GEMINI AI ==================
def askAI(question):
    global conversation_history

    try:
        model = genai.GenerativeModel("models/gemini-flash-latest")

        conversation_history.append({"role": "user", "parts": [question]})
        conversation_history = conversation_history[-MAX_HISTORY:]

        response = model.generate_content(conversation_history)
        answer = response.text.strip()

        conversation_history.append({"role": "model", "parts": [answer]})
        conversation_history = conversation_history[-MAX_HISTORY:]

        preview = answer.split(".")[0] + "."
        eel.DisplayAssistantMessage(preview)
        speak(answer)

    except Exception as e:
        eel.DisplayAssistantMessage("AI service unavailable.")
        speak("I’m having trouble connecting right now.")
        print(f"[Gemini Error] {e}")

# ================== MAIN ROUTER ==================
@eel.expose
def handleDynamicQuery(query):
    query = query.lower().strip()
    print(f"[USER QUERY] {query}")

    # Wake word
    if query in ["hey chitti", "hi chitti", "hello chitti"]:
        greeting = get_time_based_greeting()
        eel.DisplayAssistantMessage(f"{greeting}, I’m listening 👂")
        speak(f"{greeting}. I’m listening.")
        return

    # Greetings
    if query in ["hello", "hi", "hey"]:
        greeting = get_time_based_greeting()
        eel.DisplayAssistantMessage("Hello! 👋")
        speak(f"{greeting}! How can I help you today?")
        return

    # Thanks
    if any(x in query for x in ["thank you", "thanks", "thx"]):
        eel.DisplayAssistantMessage("You're welcome 😊")
        speak("You're welcome. Happy to help.")
        return
# Farewell + Exit
    if any(x in query for x in ["bye", "goodbye", "see you", "farewell", "exit", "quit"]):

        greeting = get_time_based_greeting()
        message = (
            "Good night, take care!"
            if greeting == "Good night"
            else "Goodbye! Have a great day!"
        )

        eel.DisplayAssistantMessage("Goodbye! 👋")
        speak(message)

        def shutdown():
            while is_speaking:
                time.sleep(0.1)

            eel.forceCloseWindow()
            os._exit(0)

        threading.Thread(target=shutdown, daemon=True).start()
        return

    # Identity
    if any(x in query for x in ["who are you", "what are you", "introduce yourself", "hu r u"]):
        eel.DisplayAssistantMessage("I’m Chitti, your AI voice assistant 🤖")
        speak(
            "I am Chitti, your AI voice assistant. "
            "I am here to assist you with your questions, tasks, and searches. "
            "How can I help you today?"
        )
        return

    # Incomplete open
    if query == "open":
        eel.DisplayAssistantMessage("What would you like me to open?")
        speak("What would you like me to open?")
        return

    # Open apps / sites
    if "open" in query:
        openAppOrWebsite(query)
        return

    # Search
    if any(w in query for w in ["search", "find", "look up", "google"]):
        searchWeb(query)
        return

    # YouTube
    if "play" in query and "youtube" in query:
        playYouTube(query)
        return

    # Default → Gemini
    askAI(query)