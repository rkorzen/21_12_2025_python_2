import sys

name = "World"
if len(sys.argv) > 1:
    name = sys.argv[1]

print(f"Hello {name} from python and docker")