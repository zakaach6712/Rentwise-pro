# models/property.py
from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from models import Base, CRUDMixin, TimestampMixin


class Property(CRUDMixin, TimestampMixin, Base):
    __tablename__ = "properties"

    # Collision-proof private mapped columns
    _address_col: Mapped[str] = mapped_column(
        "address", String(255), nullable=False, unique=True
    )
    _monthly_rent_col: Mapped[int] = mapped_column(
        "monthly_rent", Integer, nullable=False
    )
    _is_available_col: Mapped[bool] = mapped_column(
        "is_available", Boolean, default=True, nullable=False
    )
    _property_type_col: Mapped[Optional[str]] = mapped_column(
        "property_type", String(50), default="apartment", nullable=True
    )

    # Relationships
    leases: Mapped[List["Lease"]] = relationship(
        "Lease", back_populates="property", cascade="all, delete-orphan"
    )

    # Public accessors with validation
    @property
    def address(self) -> str:
        return self._address_col

    @address.setter
    def address(self, value: str) -> None:
        if not isinstance(value, str) or len(value.strip()) < 5:
            raise ValueError("address must be a non-empty string of at least 5 characters.")
        self._address_col = value.strip()

    @property
    def monthly_rent(self) -> int:
        return self._monthly_rent_col

    @monthly_rent.setter
    def monthly_rent(self, value: int) -> None:
        try:
            rent_int = int(value)
        except (TypeError, ValueError):
            raise ValueError("monthly_rent must be an integer.")
        if rent_int <= 0:
            raise ValueError("monthly_rent must be a positive integer.")
        self._monthly_rent_col = rent_int

    @property
    def is_available(self) -> bool:
        return self._is_available_col

    @is_available.setter
    def is_available(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError("is_available must be a boolean.")
        self._is_available_col = value

    @property
    def property_type(self) -> Optional[str]:
        return self._property_type_col

    @property_type.setter
    def property_type(self, value: Optional[str]) -> None:
        if value is not None:
            if not isinstance(value, str):
                raise ValueError("property_type must be a string if provided.")
            if len(value.strip()) < 3:
                raise ValueError("property_type must be at least 3 characters.")
            self._property_type_col = value.strip()
        else:
            self._property_type_col = None

    def __repr__(self) -> str:
        return (
            f"<Property id={self.id} "
            f"address='{self.address}' "
            f"rent={self.monthly_rent} "
            f"available={self.is_available} "
            f"type='{self.property_type}'>"
        )
