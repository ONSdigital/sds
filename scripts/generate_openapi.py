import argparse

import yaml
from fastapi.openapi.utils import get_openapi
from uvicorn.importer import import_from_string

parser = argparse.ArgumentParser(prog="generate_openapi.py")
parser.add_argument(
    "app", help='App import string. Eg. "src.app.app:app"', default="src.app.app:app"
)
parser.add_argument(
    "--out", help="Output file ending in .yaml", default="generate_openapi/openapi.yaml"
)

if __name__ == "__main__":
    args = parser.parse_args()

    print(f"importing app from {args.app}")
    app = import_from_string(args.app)
    openapi = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    version = openapi.get("openapi", "unknown version")

    print(f"writing openapi spec v{version}")

    if not args.out.endswith(".yaml"):
        print(f"Error, only yaml file is accepted")
        quit()

    with open(args.out, "w") as f:
        yaml.dump(openapi, f, sort_keys=False)

    print(f"spec written to {args.out}")
