from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from .operations import Operation, Step


@dataclass(frozen=True)
class Expression:
    operands: Tuple[int, ...]
    operations: Tuple[Operation, ...]

    def __post_init__(self) -> None:
        if len(self.operands) - 1 != len(self.operations):
            raise ValueError("Expression requires one fewer operation than operands")
        for value in self.operands:
            if value <= 0:
                raise ValueError("Operands must be positive integers")

    @property
    def steps(self) -> Tuple[Step, ...]:
        result_steps: List[Step] = []
        current = self.operands[0]
        for index, operation in enumerate(self.operations, start=1):
            right = self.operands[index]
            step = Step(current, operation, right)
            current = step.result()
            result_steps.append(step)
        return tuple(result_steps)

    @property
    def result(self) -> int:
        current = self.operands[0]
        for step in self.steps:
            current = step.result()
        return current

    def display(self, include_result: bool = False) -> str:
        if not self.operations:
            expression_body = str(self.operands[0])
        else:
            current = str(self.operands[0])
            for index, operation in enumerate(self.operations, start=1):
                operand_text = str(self.operands[index])
                current = f"({current} {operation.symbol} {operand_text})"
            expression_body = current if len(self.operations) > 1 else current[1:-1]
        if include_result:
            return f"{expression_body} = {self.result}"
        return f"{expression_body} ="
