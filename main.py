import json
from os import environ
import speech_recognition as sr
import io, os, sys
from data.models import Area, UnitArea
from init import Endpoint


obj = json.load(io.FileIO("areas.json"))
area = Area(obj.current, obj.locations)

Endpoint(area).record_request(True)
