# models/lease.py
from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date
from typing import Optional, List
from models import Base, CRUDMixin, TimestampMixin


class Lease(CRUDMixin, TimestampMixin, Base):
    __tablename__ = "leases"

    # Foreign keys
    property_id: Mapped[int] = mapped_column(
        ForeignKey("properties.id"), nullable=False
    )
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id"), nullable=False
    )

    # Internal date columns (safe names)
    _start_date: Mapped[date] = mapped_column("start_date", Date, nullable=False)
    _end_date: Mapped[Optional[date]] = mapped_column("end_date", Date, nullable=True)

    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)

    # Relationships
    property: Mapped["Property"] = relationship("Property", back_populates="leases")
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="leases")
    payments: Mapped[List["Payment"]] = relationship(
        "Payment", back_populates="lease", cascade="all, delete-orphan"
    )

    # Hybrid properties for clean access & query support
    @hybrid_property
    def lease_start(self) -> date:
        return self._start_date

    @lease_start.setter
    def lease_start(self, value: date) -> None:
        if not isinstance(value, date):
            raise ValueError("start_date must be a date instance.")
        self._start_date = value

    @hybrid_property
    def lease_end(self) -> Optional[date]:
        return self._end_date

    @lease_end.setter
    def lease_end(self, value: Optional[date]) -> None:
        if value is not None:
            if not isinstance(value, date):
                raise ValueError("end_date must be a date or None.")
            if value <= self._start_date:
                raise ValueError("end_date must be after start_date.")
        self._end_date = value

    def __repr__(self) -> str:
        return (
            f"<Lease id={self.id} property_id={self.property_id} "
            f"tenant_id={self.tenant_id} start={self._start_date} "
            f"end={self._end_date} status='{self.status}'>"
        )
