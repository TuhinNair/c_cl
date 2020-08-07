# Run

    python3 c_cl.py --file=<ROUTES FILE>

If no arguments are provided it will load routes from `routes.csv` at the root of the application folder.

# Notes

Naive implementation of shortest path algorithm. Possible considerations:
* State is maintained by proxy of list membership and checks involve list traversal. 
* There are much better algorithms for single source path.
* Front-loading computation on route load for UX.

No virtualization as no external libs were used. Considered using a python docker image but then that'd still have a prerequisite, i.e Docker.

# Tests

    python3 test_routes.py