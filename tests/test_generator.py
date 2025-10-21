from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from arithmetic_generator.cli import generate_and_save, main as cli_main
from arithmetic_generator.generator import ArithmeticGenerator, GeneratorConfig
from arithmetic_generator.operations import Operation


class ArithmeticGeneratorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.config = GeneratorConfig(
            operations=(Operation.ADD, Operation.SUB, Operation.MUL, Operation.DIV),
            operand_counts=(2, 3),
        )
        self.generator = ArithmeticGenerator(self.config, seed=42)

    def test_generate_respects_bounds(self) -> None:
        expressions = self.generator.generate(50)
        for expr in expressions:
            values = [step.result() for step in expr.steps]
            for value in values:
                self.assertGreaterEqual(value, self.config.min_value)
                self.assertLessEqual(value, self.config.max_value)

    def test_division_results_are_integer(self) -> None:
        config = GeneratorConfig(operations=(Operation.DIV,), operand_counts=(2,))
        generator = ArithmeticGenerator(config, seed=7)
        expressions = generator.generate(20)
        for expr in expressions:
            step = expr.steps[0]
            self.assertEqual(step.left % step.right, 0)
            self.assertIsInstance(step.result(), int)

    def test_cli_generates_expected_csv_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "sample.csv"
            args = type(
                "Args",
                (),
                {
                    "count": 12,
                    "operations": (Operation.ADD, Operation.SUB),
                    "operands": (2,),
                    "columns": 4,
                    "output": output_path,
                    "seed": 123,
                    "include_results": False,
                },
            )()
            generate_and_save(args)
            self.assertTrue(output_path.exists())

            with output_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.reader(handle))
            self.assertEqual(len(rows), 3)
            self.assertTrue(all(len(row) == 4 for row in rows))


class CliMainTest(unittest.TestCase):
    def test_cli_main_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "practice.csv"
            exit_code = cli_main(
                [
                    "--count",
                    "5",
                    "--operations",
                    "add,sub",
                    "--operands",
                    "2",
                    "--columns",
                    "5",
                    "--output",
                    str(output_path),
                    "--seed",
                    "99",
                ]
            )
            self.assertEqual(exit_code, 0)
            self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
