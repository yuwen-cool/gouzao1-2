from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

from .expression import Expression
from .operations import Operation


@dataclass(frozen=True)
class GeneratorConfig:
    operations: Tuple[Operation, ...]
    operand_counts: Tuple[int, ...]
    min_value: int = 1
    max_value: int = 99
    max_attempts: int = 500

    def __post_init__(self) -> None:
        if not self.operations:
            raise ValueError("At least one operation must be provided")
        if not self.operand_counts:
            raise ValueError("At least one operand count must be provided")
        for count in self.operand_counts:
            if count < 2:
                raise ValueError("Operand counts must be >= 2")
        if self.min_value <= 0 or self.max_value <= 0:
            raise ValueError("Value bounds must be positive")
        if self.min_value >= self.max_value:
            raise ValueError("Minimum value must be less than maximum value")


class ArithmeticGenerator:
    def __init__(self, config: GeneratorConfig, seed: int | None = None) -> None:
        self._config = config
        self._rng = random.Random(seed)

    def generate(self, count: int) -> Tuple[Expression, ...]:
        expressions: List[Expression] = []
        for _ in range(count):
            operand_count = self._rng.choice(self._config.operand_counts)
            expression = self._generate_expression(operand_count)
            expressions.append(expression)
        return tuple(expressions)

    def _generate_expression(self, operand_count: int) -> Expression:
        for _ in range(self._config.max_attempts):
            operations = tuple(self._rng.choice(self._config.operations) for _ in range(operand_count - 1))
            operands = [self._rng.randint(self._config.min_value, self._config.max_value)]
            current = operands[0]
            valid = True

            for operation in operations:
                candidates = self._valid_operands(current, operation)
                if not candidates:
                    valid = False
                    break
                operand = self._rng.choice(candidates)
                operands.append(operand)
                current = operation.apply(current, operand)
                if not self._is_within_bounds(current):
                    valid = False
                    break

            if valid:
                return Expression(tuple(operands), operations)
        raise RuntimeError("Unable to generate a valid expression within attempt limit")

    def _valid_operands(self, current: int, operation: Operation) -> Tuple[int, ...]:
        min_value, max_value = self._config.min_value, self._config.max_value
        if operation is Operation.ADD:
            upper = max_value - current
            if upper < min_value:
                return tuple()
            return tuple(range(min_value, upper + 1))
        if operation is Operation.SUB:
            upper = current - min_value
            if upper < min_value:
                return tuple()
            return tuple(range(min_value, current))
        if operation is Operation.MUL:
            if current == 0:
                return tuple()
            upper = max_value // current
            if upper < min_value:
                return tuple()
            return tuple(range(min_value, upper + 1))
        if operation is Operation.DIV:
            candidates: List[int] = []
            for operand in range(min_value, max_value + 1):
                if operand == 0:
                    continue
                if current % operand != 0:
                    continue
                result = current // operand
                if result < min_value or result > max_value:
                    continue
                candidates.append(operand)
            return tuple(candidates)
        raise ValueError(f"Unsupported operation: {operation}")

    def _is_within_bounds(self, value: int) -> bool:
        return self._config.min_value <= value <= self._config.max_value
