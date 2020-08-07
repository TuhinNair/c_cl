import unittest
from routes import Routes, InvalidRouteError, InvalidInputFile


class GraphInitializationTest(unittest.TestCase):
    def test_successful_graph_initialization(self):
        routes = Routes.load_routes('test_csv_files/test_routes_1.csv')
        self.assertEqual(routes.graph.edges['A'], ['B', 'C'])
        self.assertEqual(routes.graph.edges['C'], ['F'])
        self.assertEqual(routes.graph.edges['B'], [])

    def test_failed_csv_lex(self):
        with self.assertRaises(IndexError):
            Routes.load_routes('test_csv_files/incomplete_row.csv')

    def test_failed_csv_parse(self):
        with self.assertRaises(ValueError):
            Routes.load_routes('test_csv_files/wrong_duration_format.csv')

    def test_failed_illogical_route_durations(self):
        with self.assertRaises(InvalidRouteError):
            Routes.load_routes('test_csv_files/negative_duration.csv')
        with self.assertRaises(InvalidRouteError):
            Routes.load_routes('test_csv_files/impossible_cycle.csv')
        with self.assertRaises(InvalidRouteError):
            Routes.load_routes('test_csv_files/impossible_unique_nodes.csv')
    
    def test_load_empty_csv(self):
        with self.assertRaises(InvalidInputFile):
            Routes.load_routes('test_csv_files/empty.csv')


class ShortestPathTest(unittest.TestCase):
    def test_shortest_path_base_case(self):
        routes = Routes.load_routes('test_csv_files/base_case.csv')
        res = routes.graph.shortest_path('A', 'A')
        self.assertEqual(res.path, ['A'])
        self.assertEqual(res.duration, 0)

    def test_simple_shortest_path(self):
        routes = Routes.load_routes('test_csv_files/simple_path.csv')
        res = routes.graph.shortest_path('A', 'T')
        self.assertEqual(res.path, ['A', 'B', 'T'])
        self.assertEqual(res.duration, 2)

    def test_use_end_node_as_start(self):
        routes = Routes.load_routes('test_csv_files/simple_path.csv')
        res = routes.graph.shortest_path('T', 'A')
        assert res is None

    def test_no_path(self):
        routes = Routes.load_routes('test_csv_files/simple_path.csv')
        res = routes.graph.shortest_path('T', 'A')
        assert res is None
    
    def test_competing_routes(self):
        routes = Routes.load_routes('test_csv_files/simple_path_1.csv')
        res = routes.graph.shortest_path('A', 'Z')
        self.assertEqual(res.path, ['A', 'B', 'Z'])
        self.assertEqual(res.duration, 2)

    def test_unreachable_node(self):
        routes = Routes.load_routes('test_csv_files/unreachable.csv')
        res = routes.graph.shortest_path('A', 'R')
        assert res is None

if __name__ == '__main__':
    unittest.main()
