from tomlkit import parse

with open("pyproject.toml", "r") as f:
    pyproject = parse(f.read())
    print(pyproject["project"]["version"])