from __future__ import annotations
import csv
from dataclasses import dataclass
from collections import defaultdict
from typing import List


# Dynamic attributes can trigger pylint. I'm disabling it here just for convenience.
# pylint: disable=E1101


class InvalidRouteError(Exception):
    def __init__(self, message: str, line_idx: int, bad_data: list):
        self.message = "\n\n{}\nError found at line number {} of the CSV file.\n        {}".format(
            message, line_idx, bad_data)
        super().__init__(self.message)


# Perhaps this can be refactored out but it's easy immutability
@dataclass(frozen=True)
class Route:
    src: str
    dest: str
    dist: int


@dataclass
class Routes:
    def __init__(self, routes_reader):
        self.graph: RouteGraph = RouteGraph()
        for idx, raw_route in enumerate(routes_reader):
            # Malformed CSV errors causing index range errors and invalid int literal erros will panic with the default trace
            src = raw_route[0].upper()
            dest = raw_route[1].upper()
            dist = int(raw_route[2])
            unique_nodes = src == dest

            # Ideally these checks should be a part of Route and error handling/printing should have a more robust mechanism.
            # Here for now because of easy access to index and malformed data
            if unique_nodes and dist != 0:
                raise InvalidRouteError(
                    "Distance must be 0 if source and destination are the same.", idx+1, raw_route)

            if dist < 0:
                raise InvalidRouteError(
                    "Distance must be either 0 or a postive integer.", idx+1, raw_route)

            if not unique_nodes and dist == 0:
                raise InvalidRouteError(
                    "Distance between two unique nodes must be greater than 0", idx+1, raw_route)

            route = Route(src, dest, dist)
            self.graph.add_route(route)

    @staticmethod
    def load_routes(filename: str = 'routes.csv') -> Routes:
        all_routes: Routes
        with open(filename, newline='') as routes:
            reader = csv.reader(routes)
            all_routes = Routes(reader)
        return all_routes


class RouteGraph:
    def __init__(self):
        self.edges = defaultdict(list)
        self.distances = {}

    def add_route(self, r: Route):
        # Assumption is these are directed edges. The document mentioned a "starting station" and "ending station"
        self.edges[r.src].append(r.dest)
        self.distances[(r.src, r.dest)] = r.dist
