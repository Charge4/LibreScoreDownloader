import subprocess

def bump_version(file_path="version.txt"):
    with open(file_path, "r") as f:
        ver = f.read().strip()
    major, minor, patch = ver.split(".")
    patch = str(int(patch) + 1)
    new_ver = ".".join([major, minor, patch])
    with open(file_path, "w") as f:
        f.write(new_ver)
    return new_ver

def git_commit_push(version):
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"Update to version {version}"])
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    new_version = bump_version()
    print(f"New version: {new_version}")
    git_commit_push(new_version)
