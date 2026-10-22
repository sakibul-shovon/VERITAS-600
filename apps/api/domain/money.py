"""Decimal-safe Monetary Arithmetic for Trade Finance."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Union


@dataclass(frozen=True)
class Money:
    """Immutable, currency-aware Decimal monetary value.
    
    Prevents floating-point rounding anomalies in LC amounts and tolerances.
    """
    amount: Decimal
    currency: str = "USD"

    @classmethod
    def from_value(cls, val: Union[float, int, str, Decimal], currency: str = "USD") -> Money:
        if isinstance(val, Decimal):
            d = val
        else:
            d = Decimal(str(val))
        return cls(amount=d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), currency=currency.upper())

    def add_percentage(self, pct: Union[float, Decimal]) -> Money:
        factor = Decimal("1.0") + (Decimal(str(pct)) / Decimal("100.0"))
        return Money((self.amount * factor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), self.currency)

    def multiply_percentage(self, pct: Union[float, Decimal]) -> Money:
        factor = Decimal(str(pct)) / Decimal("100.0")
        return Money((self.amount * factor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), self.currency)

    def to_float(self) -> float:
        return float(self.amount)

    def __str__(self) -> str:
        return f"{self.currency} {self.amount:,.2f}"

    def __lt__(self, other: Money) -> bool:
        self._check_curr(other)
        return self.amount < other.amount

    def __le__(self, other: Money) -> bool:
        self._check_curr(other)
        return self.amount <= other.amount

    def __gt__(self, other: Money) -> bool:
        self._check_curr(other)
        return self.amount > other.amount

    def __ge__(self, other: Money) -> bool:
        self._check_curr(other)
        return self.amount >= other.amount

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False
        return self.currency == other.currency and self.amount == other.amount

    def _check_curr(self, other: Money) -> None:
        if self.currency != other.currency:
            raise ValueError(f"Currency mismatch: {self.currency} vs {other.currency}")
