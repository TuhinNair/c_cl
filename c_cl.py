from routes import Routes

if __name__ == "__main__":
    routes = Routes.load_routes()
    print(routes.shortest_path('A', 'F'))