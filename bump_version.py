def bump_version(file_path="version.txt"):
    with open(file_path, "r") as f:
        ver = f.read().strip()
    major, minor, patch = ver.split(".")
    patch = str(int(patch) + 1)
    new_ver = ".".join([major, minor, patch])
    with open(file_path, "w") as f:
        f.write(new_ver)
    return new_ver

new_version = bump_version()
print(f"New version: {new_version}")
