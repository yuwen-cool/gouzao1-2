from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable, List, Sequence

from .expression import Expression
from .generator import ArithmeticGenerator, GeneratorConfig
from .operations import Operation


def parse_operations(raw: str) -> Sequence[Operation]:
    parts = [part.strip().upper() for part in raw.split(",") if part.strip()]
    if not parts:
        raise argparse.ArgumentTypeError("Provide at least one operation")
    operations: List[Operation] = []
    for part in parts:
        try:
            operations.append(Operation[part])
        except KeyError as exc:  # pragma: no cover - argparse message path
            raise argparse.ArgumentTypeError(f"Unsupported operation '{part}'") from exc
    return operations


def parse_operand_counts(raw: str) -> Sequence[int]:
    parts = [part.strip() for part in raw.split(",") if part.strip()]
    if not parts:
        raise argparse.ArgumentTypeError("Provide at least one operand count")
    counts: List[int] = []
    for part in parts:
        value = int(part)
        if value < 2:
            raise argparse.ArgumentTypeError("Operand counts must be >= 2")
        counts.append(value)
    return counts


def chunked(items: Sequence[str], size: int) -> Iterable[Sequence[str]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate arithmetic practice problems and save them as CSV.")
    parser.add_argument("--count", type=int, default=30, help="Number of problems to generate (default: 30)")
    parser.add_argument(
        "--operations",
        type=parse_operations,
        default=parse_operations("ADD,SUB"),
        help="Comma-separated operations (ADD,SUB,MUL,DIV)",
    )
    parser.add_argument(
        "--operands",
        type=parse_operand_counts,
        default=parse_operand_counts("2"),
        help="Comma-separated operand counts (e.g., '2,3')",
    )
    parser.add_argument("--columns", type=int, default=5, help="Number of problems per CSV row (default: 5)")
    parser.add_argument("--output", type=Path, default=Path("output.csv"), help="Destination CSV path")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible output")
    parser.add_argument("--include-results", action="store_true", help="Include answers in the CSV cells")
    return parser


def expression_to_cell(expression: Expression, include_result: bool) -> str:
    return expression.display(include_result=include_result)


def write_csv(path: Path, expressions: Sequence[Expression], columns: int, include_results: bool) -> None:
    cells = [expression_to_cell(expr, include_results) for expr in expressions]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        for row in chunked(cells, columns):
            writer.writerow(row)


def generate_and_save(args: argparse.Namespace) -> Path:
    config = GeneratorConfig(operations=tuple(args.operations), operand_counts=tuple(args.operands))
    generator = ArithmeticGenerator(config=config, seed=args.seed)
    expressions = generator.generate(args.count)
    write_csv(args.output, expressions, args.columns, args.include_results)
    return args.output


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)
    output_path = generate_and_save(args)
    print(f"Generated {args.count} problems at {output_path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
