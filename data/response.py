import string
import sys, io, os, socket

class SuccessResult:
    def __init__(self, request: str) -> None:
        self.object = request

    def __str__(self):
        return self.object + "; Request successfuly created."

class FailedResult:
    def __init__(self, request: str) -> None:
        self.object = request

    def __str__(self):
        return self.object + "; Request failed for external reasons or such."

class ErrorResult:
    def __init__(self, request: str) -> None:
        self.object = request

    def __str__(self):
        return self.object + "; Request yields error."