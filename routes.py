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


# Perhaps this can be refactored out but it's easy immutability
@dataclass(frozen=True)
class Route:
    src: str
    dest: str
    duration: int


@dataclass
class Routes:
    def __init__(self, routes_reader):
        self.graph: RouteGraph = RouteGraph()
        for idx, raw_route in enumerate(routes_reader):
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

    def shortest_path(self, start: str, end: str) -> Optional[Result]:
        return self.graph._shortest_path(start, end)

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
        self.durations = {}

    def add_route(self, r: Route):
        # Assumption is these are directed edges. The document mentioned a "starting station" and "ending station"
        self.edges[r.src].append(r.dest)
        self.durations[(r.src, r.dest)] = r.duration

    def _shortest_path(self, start, end) -> Optional[Result]:
        if start not in self.edges.keys():
            return None
        if start == end:
            return Result([start], 0)
        unvisited = [*self.edges]
        visited = []
        duration_from_start = {}
        duration_from_start[start] = 0
        last_edge = {}

        while unvisited:
            print("\nUnvisited: {}".format(unvisited))
            leftover_edges = {k:v for (k,v) in duration_from_start.items() if k in unvisited}
            current_shortest = min(leftover_edges, key=leftover_edges.get)
            print("Current Shortet: {}\n".format(current_shortest))
            for neighbor in self.edges[current_shortest]:
                print("Checking neighbour: {}\n".format(neighbor))
                if neighbor not in visited:
                    local_duration = self.durations[(
                        current_shortest, neighbor)]
                    print("local duration from {} to {} is {}\n".format(current_shortest, neighbor, local_duration))
                    global_duration = duration_from_start[current_shortest] + \
                        local_duration
                    if neighbor not in duration_from_start:
                        duration_from_start[neighbor] = global_duration
                        last_edge[neighbor] = current_shortest
                        print("Adding DFS for edge {} with duration {}\n".format(neighbor, global_duration))
                    elif duration_from_start[neighbor] > global_duration:
                        duration_from_start[neighbor] = global_duration
                        last_edge[neighbor] = current_shortest
                        print("Updating DFS for edge {} with duration {}\n".format(neighbor, global_duration))
            print("Duration from start: {}\n".format(duration_from_start))
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


@dataclass(frozen=True)
class Result:
    path: List[str]
    duration: int

    def __str__(self):
        stops = 0
        path_len = len(self.path)

        if path_len >= 1:
            stops = path_len

        return "Result: {} stops, {} minutes".format(stops, self.duration)
