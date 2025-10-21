from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable


class Operation(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"

    @property
    def symbol(self) -> str:
        return self.value

    def apply(self, left: int, right: int) -> int:
        if self is Operation.ADD:
            return left + right
        if self is Operation.SUB:
            return left - right
        if self is Operation.MUL:
            return left * right
        if self is Operation.DIV:
            if right == 0 or left % right != 0:
                raise ValueError("Division requires a non-zero divisor and integer result")
            return left // right
        raise ValueError(f"Unsupported operation: {self}")


@dataclass(frozen=True)
class Step:
    left: int
    operation: Operation
    right: int

    def result(self) -> int:
        return self.operation.apply(self.left, self.right)
