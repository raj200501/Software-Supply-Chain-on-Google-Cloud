#!/usr/bin/env python3
import argparse
import json
import sys

REQUIRED_BUILDER_PREFIX = "https://cloudbuild.googleapis.com/"
REQUIRED_BUILD_TYPE = "https://bazel.build"

def verify(path: str) -> None:
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if data.get("_type") != "https://slsa.dev/provenance/v1":
        raise SystemExit("unexpected predicate type")
    predicate = data.get("predicate", {})
    if predicate.get("buildType") != REQUIRED_BUILD_TYPE:
        raise SystemExit("unexpected build type")
    builder_id = predicate.get("builder", {}).get("id", "")
    if not builder_id.startswith(REQUIRED_BUILDER_PREFIX):
        raise SystemExit("builder id is not Cloud Build")
    recipe = predicate.get("recipe", {})
    if "//" not in recipe.get("entryPoint", ""):
        raise SystemExit("entryPoint must reference a Bazel target")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    try:
        verify(args.path)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"verification failed: {exc}", file=sys.stderr)
        sys.exit(1)
    print("provenance verified")
