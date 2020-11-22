import sys
import os

reqs = sys.argv[1:]
if len(reqs) == 0:
    exit()

cols = ["A", "E", "I"]

def COL_REF(c: str) -> str:
    return f"${c}:${c}"

def COLROW(c: str, r: str) -> str:
    return f"{c}{r}"

def IFNA(r: str, e: str) -> str:
    return f"IFNA({r}, {e})"

def INDIRECT(r: str) -> str:
    return f"INDIRECT({r})"

def ADDRESS(r, c: str) -> str:
    return f"ADDRESS({r}, {c})"

def FLOOR(r: str) -> str:
    return f"FLOOR({r})"

def COLUMN(r: str) -> str:
    return f"COLUMN({r})"

def MATCH(r: str, c: str, t: str) -> str:
    return f"MATCH({r}, {c}, {t})"

def NA() -> str:
    return "NA()"

def MULTIPLY(a, b: str) -> str:
    return f"MULTIPLY({a}, {b})"

def DIVIDE(a, b: str) -> str:
    return f"DIVIDE({a}, {b})"

def ADD(a, b: str) -> str:
    return f"ADD({a}, {b})"

def STRING(a: str) -> str:
    return f"\"{a}\""

def EQUALS(a, b: str) -> str:
    return f"{a} = {b}"

def IF(a, b, c: str) -> str:
    return f"IF({a}, {b}, {c})"

columns_unmapped = [0, 10, 20, 30, 40]
columns_mapped = [1, 11, 20, 29, 38]
def get_nearest(n: str, cu, cm: list) -> str:
    v = EQUALS(n, cu[0])

    if len(cu) == 1:
        return IF(v, cm[0], NA())
    return IF(v, cm[0], get_nearest(n, cu[1:], cm[1:]))

def generate_per_col(s: str, c: list) -> str:
    m = MATCH(STRING(s), COL_REF(c[0]), 0)
    div = DIVIDE(m, 10)
    f = FLOOR(div)
    x = MULTIPLY(10, f)
    a = get_nearest(x, columns_unmapped, columns_mapped)
    v = INDIRECT(ADDRESS(a, COLUMN(COLROW(c[0], 1))))

    if len(c) == 1:
        return IFNA(v, NA())
    return IFNA(v, generate_per_col(s, c[1:]))

def generate(r: list) -> str:
    course = r[0]
    v = generate_per_col(course, cols)

    if len(r) == 1:
        return IFNA(v, STRING("Unplanned"))
    return IFNA(v, generate(r[1:]))


print(generate(reqs))


