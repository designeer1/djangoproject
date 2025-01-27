import pyttsx3
from elevenlabs import generate, play
import comtypes

def initialize_engine():
    """Initialize text-to-speech engine"""
    comtypes.CoInitialize()
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', engine.getProperty('rate') - 50)
    engine.setProperty('volume', engine.getProperty('volume') + 0.25)
    return engine

def engine_talk(query):
    """Generate speech from text"""
    audio = generate(text=query, voice='Aria', model="eleven_monolingual_v1")
    play(audio)

def finalize_engine():
    # Clean up COM resources after the operation
    comtypes.CoUninitialize()

