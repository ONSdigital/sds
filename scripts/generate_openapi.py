import argparse
import sys

import yaml
from uvicorn.importer import import_from_string

parser = argparse.ArgumentParser(prog="generate_openapi.py")
parser.add_argument(
    "app", help='App import string. Eg. "app.main:app"', default="app.main:app"
)
parser.add_argument(
    "--out", help="Output file ending in .yaml", default="gateway/openapi.yaml"
)

if __name__ == "__main__":
    args = parser.parse_args()

    print(f"importing app from {args.app}")
    app = import_from_string(args.app)
    openapi = app.openapi()

    if not args.out.endswith(".yaml"):
        print("Error, only yaml file is accepted")
        sys.exit()

    with open(args.out, "w") as f:
        yaml.dump(openapi, f, sort_keys=False)

    print(f"spec written to {args.out}")
