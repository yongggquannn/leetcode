from _harness import load

m = load("problem_3_word_search")

BOARD = [
    ["A", "B", "C", "E"],
    ["S", "F", "C", "S"],
    ["A", "D", "E", "E"],
]


def _valid_path(board, word, path, diagonal=False):
    if path is None or len(path) != len(word) or len(set(path)) != len(path):
        return False
    for i, (r, c) in enumerate(path):
        if board[r][c] != word[i]:
            return False
        if i:
            pr, pc = path[i - 1]
            dr, dc = abs(r - pr), abs(c - pc)
            ok = max(dr, dc) == 1 if diagonal else dr + dc == 1
            if not ok:
                return False
    return True


# ---- Part 1
def test_part1_examples():
    assert m.exists(BOARD, "ABCCED")
    assert m.exists(BOARD, "SEE")
    assert not m.exists(BOARD, "ABCB"), "a cell can't be reused"


def test_part1_edges():
    assert m.exists(BOARD, "")
    assert not m.exists([], "A")
    assert m.exists([["A"]], "A")
    assert not m.exists([["A"]], "AA")
    assert not m.exists(BOARD, "ABCCEDX")


def test_part1_backtracks_correctly():
    board = [["A", "A", "A"], ["A", "B", "A"], ["A", "A", "A"]]
    assert m.exists(board, "AAAAAAAAB")
    assert not m.exists(board, "AAAAAAAAAB")


# ---- Part 2
def test_part2_returns_valid_path():
    for word in ["ABCCED", "SEE", "ADFBCCE"]:
        path = m.find_path(BOARD, word)
        assert _valid_path(BOARD, word, path), f"{word}: {path}"


def test_part2_none_when_missing():
    assert m.find_path(BOARD, "ABCB") is None


# ---- Part 3
def test_part3_find_words():
    board = [
        ["o", "a", "a", "n"],
        ["e", "t", "a", "e"],
        ["i", "h", "k", "r"],
        ["i", "f", "l", "v"],
    ]
    assert m.find_words(board, ["oath", "pea", "eat", "rain"]) == {"oath", "eat"}


def test_part3_shared_prefixes_and_duplicates():
    board = [["a", "b"], ["c", "d"]]
    words = ["ab", "abd", "abdc", "abdca", "ac", "acdb", "ab", "bd", "x"]
    assert m.find_words(board, words) == {"ab", "abd", "abdc", "ac", "acdb", "bd"}


# ---- Part 4
def test_part4_diagonal():
    board = [["A", "X"], ["Y", "B"]]
    assert not m.exists(board, "AB")
    assert m.exists(board, "AB", diagonal=True)
    path = m.find_path(board, "AB", diagonal=True)
    assert _valid_path(board, "AB", path, diagonal=True)
    assert m.find_words(board, ["AB", "XY", "AXBY"], diagonal=True) == {"AB", "XY", "AXBY"}
    assert m.find_words(board, ["AB", "XY", "AXBY"]) == {"AXBY"}, "default stays orthogonal"
