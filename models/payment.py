# models/payment.py
from sqlalchemy import Numeric, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Optional
from models import Base, CRUDMixin, TimestampMixin


class Payment(CRUDMixin, TimestampMixin, Base):
    __tablename__ = "payments"

    # Foreign key to Lease
    lease_id: Mapped[int] = mapped_column(
        ForeignKey("leases.id"), nullable=False
    )

    # Collision-proof private columns
    _amount_col: Mapped[Decimal] = mapped_column(
        "amount", Numeric(10, 2), nullable=False
    )
    _date_paid_col: Mapped[date] = mapped_column(
        "date_paid", Date, nullable=False
    )
    _method_col: Mapped[Optional[str]] = mapped_column(
        "method", String(20), nullable=True  # e.g. cash, mpesa, bank
    )

    # Relationships
    lease: Mapped["Lease"] = relationship(
        "Lease", back_populates="payments"
    )

    # Public accessors / validation
    @property
    def amount(self) -> Decimal:
        return self._amount_col

    @amount.setter
    def amount(self, value) -> None:
        try:
            v = Decimal(value)
        except (InvalidOperation, TypeError):
            raise ValueError("amount must be a valid decimal number.")
        if v <= 0:
            raise ValueError("Payment amount must be positive.")
        self._amount_col = v

    @property
    def date_paid(self) -> date:
        return self._date_paid_col

    @date_paid.setter
    def date_paid(self, value: date) -> None:
        if not isinstance(value, date):
            raise ValueError("date_paid must be a date object.")
        self._date_paid_col = value

    @property
    def method(self) -> Optional[str]:
        return self._method_col

    @method.setter
    def method(self, value: Optional[str]) -> None:
        if value is not None:
            if len(value.strip()) < 3:
                raise ValueError("method must be at least 3 characters if provided.")
            self._method_col = value.strip()
        else:
            self._method_col = None

    def __repr__(self) -> str:
        return (
            f"<Payment id={self.id} lease_id={self.lease_id} "
            f"amount={self.amount} date={self.date_paid} method='{self.method}'>"
        )
