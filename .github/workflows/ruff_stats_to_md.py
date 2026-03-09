from pathlib import Path

from pandas import DataFrame
from parse import Result, parse

with Path("ruff_stats.txt").open() as f:
    error_lines = f.readlines()
    rows = []
    for error_line in error_lines:
        p1 = parse("{}\t{}\t[{}] {}", error_line)
        p2 = parse("{}\t{}\t{}", error_line)
        if type(p1) is Result:
            d = {
                "Error code": p1[1],
                "Error name": p1[3],
                "Number of errors": p1[0],
                "Is fixable with `--fix`": p1[2],
            }
            rows.append(d)
        elif type(p2) is Result:
            d = {
                "Error code": p2[1],
                "Error name": p2[2],
                "Number of errors": p2[0],
            }
            rows.append(d)
    df = DataFrame(
        data=rows,
        columns=[
            "Error code",
            "Error name",
            "Number of errors",
            "Is fixable with `--fix`",
        ],
    ).fillna("")

print(df.to_markdown(index=False))
