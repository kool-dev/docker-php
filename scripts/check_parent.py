#!/usr/bin/env python3
"""Fail if a derived build replaced or did not inherit the same-job base."""

import json
import subprocess
import sys


def inspect(image):
    return json.loads(subprocess.check_output(["docker", "image", "inspect", image], text=True))[0]


def check_parent(tag, base_id, derived_id):
    base = inspect(f"kooldev/php:{tag}")
    if base["Id"] != base_id:
        raise ValueError("Local base was replaced after it was built and tested")
    derived = inspect(derived_id)
    layers = base["RootFS"]["Layers"]
    if not layers or derived["RootFS"]["Layers"][:len(layers)] != layers:
        raise ValueError("Derived image did not inherit the tested base's layers")
    print(f"{derived_id} inherits all {len(layers)} layers of tested base {base_id}")


if __name__ == "__main__":
    check_parent(*sys.argv[1:])
