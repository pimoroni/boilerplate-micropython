#!/usr/bin/env python

import argparse
import json
from pathlib import Path


def repo_url(repo_url):
    if "git@github.com:" not in repo_url and "https://github.com:" not in repo_url and len(repo_url.split("/")) != 2:
        raise argparse.ArgumentTypeError(f'"{repo_url}" is not a valid GitHub URL')
    repo_url = repo_url.replace("git@github.com:", "")
    repo_url = repo_url.replace("https://github.com:", "")
    repo_url = repo_url.replace("https://github.com/", "")
    return repo_url.removesuffix(".git")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--repo", type=repo_url, required=True)
    parser.add_argument("-v", "--ver", required=True)
    parser.add_argument("root", type=Path)
    args = parser.parse_args()

    package_json = Path("package.json")

    try:
        data = json.loads(package_json.read_text())
        print("package.json found: updating!")
    except FileNotFoundError:
        data = {}
        print("package.json not found: creating!")

    data.update({"version": args.ver, "urls": []})

    for path in sorted(args.root.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        relpath = str(path.relative_to(args.root))
        print(f"Adding {relpath} as github:{args.repo}/src/{relpath}")
        data["urls"].append([relpath, f"github:{args.repo}/src/{relpath}"])

    package_json.write_text(json.dumps(data, indent=True) + "\n")


if __name__ == "__main__":
    main()
