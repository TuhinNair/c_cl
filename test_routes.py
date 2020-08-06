import unittest
from routes import Routes, InvalidRouteError


class GraphInitializationTest(unittest.TestCase):
    def setUp(self):
        self.routes = Routes.load_routes('test_csv_files/test_routes_1.csv')

    def test_successful_graph_initialization(self):
        self.assertEqual(self.routes.graph.edges['A'], ['B', 'C'])
        self.assertEqual(self.routes.graph.edges['C'], ['F'])
        self.assertEqual(self.routes.graph.edges['B'], [])

    def test_failed_csv_lex(self):
        with self.assertRaises(IndexError):
            Routes.load_routes('test_csv_files/incomplete_row.csv')

    def test_failed_csv_parse(self):
        with self.assertRaises(ValueError):
            Routes.load_routes('test_csv_files/wrong_distance_format.csv')
    
    def test_failed_illogical_route_distances(self):
        with self.assertRaises(InvalidRouteError):
            Routes.load_routes('test_csv_files/negative_distance.csv')
        with self.assertRaises(InvalidRouteError):
            Routes.load_routes('test_csv_files/impossible_cycle.csv')
        with self.assertRaises(InvalidRouteError):
            Routes.load_routes('test_csv_files/impossible_unique_nodes.csv')


if __name__ == '__main__':
    unittest.main()
