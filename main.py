import multiprocessing
import eel
from engine.speech import speak
from engine.features import playAssistantSound
from engine.universal import handleDynamicQuery  # The new logic
import engine.command  # Ensure commands are loaded
if __name__ == "__main__":
    multiprocessing.freeze_support()
    eel.init('www')

    @eel.expose
    def process_user_query(query):
        handleDynamicQuery(query)

    eel.start('index.html', mode='chrome', size=(1200, 800))
