from __future__ import annotations
import csv
from dataclasses import dataclass
from collections import defaultdict
from typing import List, Optional
import functools


# Dynamic attributes can trigger pylint. I'm disabling it here just for convenience.
# pylint: disable=E1101


class InvalidRouteError(Exception):
    def __init__(self, message: str, line_idx: int, bad_data: list):
        self.message = "\n\n{}\nError found at line number {} of the CSV file.\n        {}".format(
            message, line_idx, bad_data)
        super().__init__(self.message)


class InvalidInputFile(Exception):
    def __init__(self):
        super().__init__("The CSV file is empty")

# Perhaps this can be refactored out but it's easy immutability


@dataclass(frozen=True)
class Route:
    src: str
    dest: str
    duration: int


@dataclass
class Routes:
    def __init__(self, route_reader):
        self.graph: RouteGraph = RouteGraph()
        for idx, raw_route in enumerate(route_reader):
            # Malformed CSV errors causing index range errors and invalid int literal erros will panic with the default trace
            src = raw_route[0].upper()
            dest = raw_route[1].upper()
            duration = int(raw_route[2])
            unique_nodes = src == dest

            # Ideally these checks should be a part of Route and error handling/printing should have a more robust mechanism.
            # Here for now because of easy access to index and malformed data

            if unique_nodes and duration != 0:
                raise InvalidRouteError(
                    "Duration must be 0 if source and destination are the same.", idx+1, raw_route)

            if duration < 0:
                raise InvalidRouteError(
                    "Duration must be either 0 or a postive integer.", idx+1, raw_route)

            if not unique_nodes and duration == 0:
                raise InvalidRouteError(
                    "Duration between two unique nodes must be greater than 0", idx+1, raw_route)

            route = Route(src, dest, duration)
            self.graph.add_route(route)

    @staticmethod
    def load_routes(filename: str = 'routes.csv') -> Routes:
        all_routes: Routes
        with open(filename, newline='') as routes:
            reader = csv.reader(routes)
            all_routes = Routes(reader)

        if not all_routes.graph.edges:
            raise InvalidInputFile()

        return all_routes


class RouteGraph:
    def __init__(self):
        self.edges = defaultdict(list)
        self.durations = {}

    def add_route(self, r: Route):
        # Assumption is these are directed edges. The document mentioned a "starting station" and "ending station"
        self.edges[r.src].append(r.dest)
        self.durations[(r.src, r.dest)] = r.duration

    def shortest_path(self, start, end) -> Optional[Result]:
        unvisited = [*self.edges]  # All nodes that can act as a starting point

        if start not in unvisited:
            return None
        if start == end:
            return Result([start], 0)

        visited = []  # All nodes that have been reached
        duration_from_start = {}
        duration_from_start[start] = 0
        last_edge = {}

        while unvisited:
            leftover_edges = {
                k: v for (k, v) in duration_from_start.items() if k in unvisited}
            if not leftover_edges:
                break
            current_shortest = min(leftover_edges, key=leftover_edges.get)
            for neighbor in self.edges[current_shortest]:
                if neighbor not in visited:
                    local_duration = self.durations[(
                        current_shortest, neighbor)]
                    global_duration = duration_from_start[current_shortest] + \
                        local_duration
                    if neighbor not in duration_from_start:
                        duration_from_start[neighbor] = global_duration
                        last_edge[neighbor] = current_shortest
                    elif duration_from_start[neighbor] > global_duration:
                        duration_from_start[neighbor] = global_duration
                        last_edge[neighbor] = current_shortest
            unvisited.remove(current_shortest)
            visited.append(current_shortest)

        if end not in duration_from_start:
            return None
        else:
            current = end
            path = [end]
            while True:
                current = last_edge[current]
                path.append(current)
                if current == start:
                    break

            return Result(path[::-1], duration_from_start[end])

    def pretty_routes(self) -> str:
        pretty = '\nFrom ---> To :  Duration\n'
        for k, v in self.durations.items():
            (src, dest) = k
            pretty += "{}   --->   {}  :  {} minutes\n".format(src, dest, v)
        return pretty


@dataclass(frozen=True)
class Result:
    path: List[str]
    duration: int

    def __str__(self):
        stops = 0
        path_len = len(self.path)

        if path_len >= 1:
            stops = path_len

        return "Result:\n {} stops, {} minutes\nPath: {}\n".format(stops, self.duration, self.path)
