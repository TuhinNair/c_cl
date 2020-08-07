from routes import Routes
import argparse
import sys


def prompt(routes: Routes):
    print(routes.graph.pretty_routes())
    while True:
        start = input("\nWhat station are you getting on the train? ")
        end = input("\nWhat starion are you getting off the train? ")

        print("\n{}".format(routes.graph.shortest_path(start.upper(), end.upper())))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A toy shortest path CLA")
    parser.add_argument('--file')
    args = parser.parse_args()
   
    if args.file:
        val = args.file
        print("\nLoading routes from: {}\n\n".format(val))
        routes = Routes.load_routes(val)
        prompt(routes)
       
    else:
        print("\nLoading default routes from routes.csv\n\n")
        routes = Routes.load_routes()
        prompt(routes)
