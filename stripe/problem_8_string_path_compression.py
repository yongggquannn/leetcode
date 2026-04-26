"""
String Path Compression (Stripe)
Source (paywalled): https://darkinterview.com/collections/t4y7u1i8/questions/da3a6991-37c1-48f9-bc68-6b8e4eee85e5
Reference: LeetCode 71 "Simplify Path", interviewing.io "Simplify Path"

Public detail is THIN; the title strongly suggests the classic Unix-style
path-simplification problem (Stripe asks the file-path variant frequently).
Confirm wording with your source.

================================================================================
PART 1: Simplify Absolute Path
================================================================================

Given an absolute Unix path string, return the canonical simplified path.

Rules:
    "."   -> current directory (skip)
    ".."  -> parent directory (pop one segment)
    "//"  -> treat as single "/"
    Trailing slash removed unless the path is "/".

Examples:
    simplify_path("/home/")         == "/home"
    simplify_path("/../")           == "/"
    simplify_path("/home//foo/")    == "/home/foo"
    simplify_path("/a/./b/../../c/")== "/c"

Approach: split on "/", push/pop a stack, join with "/".

================================================================================
PART 2: Relative paths with a current working directory
================================================================================

Function:
    simplify_path_part2(path: str, cwd: str) -> str

If `path` starts with "/", treat as absolute (Part 1 semantics).
Otherwise, resolve `path` against `cwd`.

Examples:
    simplify_path_part2("docs/../src", "/home/user") == "/home/user/src"
    simplify_path_part2("../etc",      "/home/user") == "/home/etc"
    simplify_path_part2("./a/./b",     "/")          == "/a/b"
    simplify_path_part2("/abs/path",   "/home/user") == "/abs/path"

================================================================================
PART 3: Symlink resolution
================================================================================

Function:
    simplify_path_part3(path: str, symlinks: dict[str, str]) -> str

`symlinks` maps an absolute path to its target (also absolute). When a path
prefix matches a symlink, substitute the target and continue resolving.
Detect cycles - raise ValueError or return the input unchanged.

Examples:
    symlinks = {
        "/var/www":  "/srv/http",
        "/srv/http": "/data/sites",
    }
    simplify_path_part3("/var/www/index.html", symlinks)
        == "/data/sites/index.html"

    simplify_path_part3("/var/www/../logs", symlinks)
        == "/data/logs"        # /var/www -> /srv/http -> /data/sites,
                               # then "..", giving /data, then /logs

    # Cycle:
    bad = {"/a": "/b", "/b": "/a"}
    simplify_path_part3("/a/x", bad) -> raises ValueError
"""


def simplify_path_part1(path: str) -> str:
    pass


def simplify_path_part2(path: str, cwd: str) -> str:
    pass


def simplify_path_part3(path: str, symlinks: dict[str, str]) -> str:
    pass


if __name__ == "__main__":
    pass
