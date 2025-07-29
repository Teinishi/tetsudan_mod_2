import sys


def bail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)
