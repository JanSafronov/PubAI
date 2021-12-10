import math, numpy, matplotlib
from typing import Iterable, overload
import select, collections, genericpath

class Node:
    def __init__(self, name) -> None:
        self.name = name

class UnitNode(Node):
    def __init__(self, name, references: list(Node) | Node) -> None:
        self.name = name
        self.references = references

class Location(Node):
    def __init__(self, name, latitude: float, longitude: float) -> None:
        super().__init__(name)
        self.latitude = latitude
        self.longitude = longitude

class UnitArea(Location):
    def __init__(self, name, latitude: float, longitude: float, references: list(Node) | Node) -> None:
        super().__init__(name, latitude, longitude)
        self.references = references

    def find_reference(self, name: set) -> Node:
        return self.nodes.index(Node(name))

    def reference_exists(self, name: set) -> bool:
        return self.nodes.index(Node(name)) != -1

class Area:
    def __init__(self, address: str, locations: list) -> None:
        self.address = address
        self.locations = locations

    def find_location(self, name: set) -> Node:
        return self.locations[self.locations.index(lambda unit : unit.name == name | unit.references.contains(unit.name))]

    def location_exists(self, name: set) -> bool:
        return self.locations.__contains__(lambda unit : unit.name == name | unit.references.contains(unit.name))