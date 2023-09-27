import json

__all__ = ["props"]
props = {}

with open("properties.json", "r") as f:
    props = json.loads(f.read())
