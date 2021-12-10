from os import environ
import math, numpy, matplotlib
from typing import Sequence, Union
import select, collections, genericpath
from numpy.core.records import array
from numpy.core.shape_base import stack
from openai.api_resources import engine
import speech_recognition as sr, openai
import io, os, sys
from data.models import Area
from data.response import SuccessResult

"""Endpoint representing area and current position in it with request-response handling

Returns:
    class: Endpoint
"""
class Endpoint:
    """Endpoint representing area and current position in it with request-response handling

    Returns:
        Area: Area around which unit areas the endpoint will be moving
    """
    def __init__(self, Area: Area) -> None:
        self.Area = Area
        self.Requests = list()
        self.Stops = list()
    
    """Move current unit area into the next one
    """
    def move_area(self) -> str:
        self.Area.current = self.Area.locations.pop(0)
        if self.Area.current in self.Stops:
            return "Stopping at:" + self.Area.current

    """Records requests and optionally responds back
    """
    def record_request(self, withresponse: bool) -> bool | str:
        with sr.Microphone() as mic:
            rec = sr.Recognizer()
             
            print(mic.list_working_microphones())
            
            data = rec.record(mic)
            
            text = rec.recognize_azure(data, os.environ.get("AZURE_SPEECHSERVICE_KEY"), language="he-IL", location="eastus2")

            self.Requests.append(text)
            
            if withresponse:
                return self.record_response()

            return SuccessResult()

    """Responds an operation done with the record
    """
    def record_response(self) -> str | bool:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        request = self.Requests.pop()
        
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt="The following AI is a public transport assistant. He identifies questions (in hebrew) in the request and categorizes them with respect to the following available categories: Locate, Reminder, Violence, None.\n\nRequest:" + request + "\nCategory: ",
            temperature=0.8,
            max_tokens=20,
            top_p=1,
            frequency_penalty=0.3,
            presence_penalty=0.7,
            stop=["\n", " Request:", " Category:"])

        if response.find("Locate") != -1:
            response = openai.Completion.create(
                engine="davinci-codex",
                prompt="The following AI is a public transport assistant. He identifies and returns the requested location in the request (in hebrew).\n\nRequest:" + request + "\nLocation: ",
                temperature=0.8,
                max_tokens=20,
                top_p=1,
                frequency_penalty=0.3,
                presence_penalty=0.7,
                stop=["\n", " Request:", " Location:"])

            return self.Area.location_exists(response)
        
        if response.find("Reminder") != -1:
            response = openai.Completion.create(
                engine="davinci-codex",
                prompt="The following AI is a public transport assistant. He identifies and returns the requested location (in hebrew).\n\nRequest:" + request + "\nLocation: ",
                temperature=0.8,
                max_tokens=20,
                top_p=1,
                frequency_penalty=0.3,
                presence_penalty=0.7,
                stop=["\n", " Request:", " Location:"])

            self.Stops.append(response)

            return self.Area.location_exists(response)

        return None
