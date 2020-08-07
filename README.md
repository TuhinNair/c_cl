# Run

    python3 c_cl.py --file=<ROUTES FILE>

If no arguments are provided it will load routes from `routes.csv` at the root of the application folder.

# Notes

Naive implementation of shortest path algorithm. Membership checks involve list traversal. 

No virtualization as no external libs were used. Considered using a python docker image but then that'd still have a prerequisite, i.e Docker.

# Tests

    python3 test_routes.py