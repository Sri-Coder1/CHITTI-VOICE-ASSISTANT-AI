import eel
import pyttsx3
import threading
import queue

# ================== ENGINE SETUP ==================
engine = pyttsx3.init()
engine.setProperty("rate", 165)

# Female voice (Windows)
for v in engine.getProperty("voices"):
    if "zira" in v.name.lower():
        engine.setProperty("voice", v.id)
        break

# ================== STATE ==================
speech_queue = queue.Queue()
is_speaking = False
lock = threading.Lock()

# ================== SPEECH WORKER ==================
def speech_loop():
    global is_speaking

    while True:
        text = speech_queue.get()
        if text is None:
            break

        with lock:
            is_speaking = True
            eel.setSpeakingState(True)

        engine.say(text)
        engine.runAndWait()   # 🔥 ONLY PLACE runAndWait is called

        with lock:
            is_speaking = False
            eel.setSpeakingState(False)

        speech_queue.task_done()

# ================== START BACKGROUND THREAD ==================
speech_thread = threading.Thread(target=speech_loop, daemon=True)
speech_thread.start()

# ================== PUBLIC API ==================
def speak(text):
    clear_queue()
    speech_queue.put(text)

@eel.expose
def stopSpeaking():
    global is_speaking
    clear_queue()
    if is_speaking:
        engine.stop()
        is_speaking = False
        eel.setSpeakingState(False)

def clear_queue():
    while not speech_queue.empty():
        try:
            speech_queue.get_nowait()
            speech_queue.task_done()
        except queue.Empty:
            break
