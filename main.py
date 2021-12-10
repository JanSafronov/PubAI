from os import environ
import speech_recognition as sr
import io, os, sys
from path import Area, UnitArea

area = Area("address", UnitArea("Address0", 37.32, -65.2))

with sr.Microphone() as mic:
    rec = sr.Recognizer()
    #rec.dynamic_energy_threshold = True

    print(mic.list_working_microphones())
    
    data = rec.record(mic, duration=50)
    
    text = rec.recognize_azure(data, os.environ.get("AZURE_SPEECHSERVICE_KEY"), language="he-IL", location="eastus2")

    print("here")