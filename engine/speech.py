import eel
import pyttsx3
import time

is_speaking = False


# ================== SPEECH FUNCTION ==================
def speak(text: str):
    """
    Speak text synchronously. Recreates pyttsx3 engine every call
    to avoid Windows SAPI lock issue after first speech.
    """
    global is_speaking

    if not text or not isinstance(text, str):
        return

    stopSpeaking()

    try:
        is_speaking = True
        try:
            eel.setSpeakingState(True)
        except:
            pass

        # ✅ Recreate engine fresh for every speech to prevent locking
        engine = pyttsx3.init()
        engine.setProperty("rate", 165)

        for v in engine.getProperty("voices"):
            if "zira" in v.name.lower():
                engine.setProperty("voice", v.id)
                break

        engine.say(text)
        engine.runAndWait()
        engine.stop()  # ensure loop fully closes
        del engine     # cleanup

    except Exception as e:
        print(f"[Speech Error] {e}")

    finally:
        is_speaking = False
        try:
            eel.setSpeakingState(False)
        except:
            pass


# ================== STOP SPEAKING ==================
@eel.expose
def stopSpeaking():
    """Stop any ongoing speech."""
    global is_speaking
    is_speaking = False
    try:
        eel.setSpeakingState(False)
    except:
        pass


# ================== SHUTDOWN ==================
def shutdown_speech():
    """Gracefully shutdown TTS system."""
    stopSpeaking()
    print("[Speech Engine] Shutdown complete.")
