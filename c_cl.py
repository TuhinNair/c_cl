from routes import Routes

if __name__ == "__main__":
    routes = Routes.load_routes('test_csv_files/empty.csv')
    print(routes.graph.shortest_path('A', 'F'))