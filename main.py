import eel
from engine.features import *
from engine.command import *

eel.init('www')

# Do NOT call playAssistantSound() or os.system here

eel.start('index.html', mode='chrome', host='localhost', block=True)