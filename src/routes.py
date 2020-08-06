from __future__ import annotations
import csv
from dataclasses import dataclass
from typing import List


# Dynamic attributes can trigger pylint. I'm disabling it here just for convenience.
# pylint: disable=E1101

@dataclass(frozen=True)
class Route:
    src: str
    dest: str
    dist: int

@dataclass
class Routes:
    def __init__(self, raw_routes: List[List[str]]):
        routes: List[Route] = []
        for raw_route in raw_routes:
                route = Route(raw_route[0], raw_route[1], int(raw_route[2]))
                routes.append(route)
        object.__setattr__(self, 'routes', routes)
    
    @staticmethod
    def load_routes(filename: str = 'routes.csv') -> Routes:
        all_routes: Routes
        with open(filename, newline='') as routes:
            route_reader = csv.reader(routes)
            all_routes = Routes(route_reader)
        return all_routes



