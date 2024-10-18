import re


def increase_version(version, part):
    major, minor, patch = map(int, version.split("."))
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    return f"{major}.{minor}.{patch}"


def main():
    version_file = "./yaptyper/app_version.py"
    with open(version_file, "r") as f:
        content = f.read()

    current_version = re.search(r"__version__ = \'(\d+\.\d+\.\d+)\'", content).group(1)
    new_version = increase_version(current_version, "patch")

    with open(version_file, "w") as f:
        f.write(f"__version__ = '{new_version}'\n")


if __name__ == "__main__":
    main()
