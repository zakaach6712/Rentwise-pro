# models/tenant.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models import Base, CRUDMixin, TimestampMixin


class Tenant(CRUDMixin, TimestampMixin, Base):
    __tablename__ = "tenants"

    # Collision-proof mapped columns
    _name_col: Mapped[str] = mapped_column(
        "name", String(120), nullable=False
    )
    _contact_info_col: Mapped[str] = mapped_column(
        "contact_info", String(120), nullable=False, unique=True
    )

    # Relationships
    leases: Mapped[List["Lease"]] = relationship(
        "Lease",
        back_populates="tenant",
        cascade="all, delete-orphan"
    )

    # Public accessors / validators
    @property
    def name(self) -> str:
        return self._name_col

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or len(value.strip()) < 2:
            raise ValueError("name must be a string with at least 2 characters.")
        self._name_col = value.strip()

    @property
    def contact_info(self) -> str:
        return self._contact_info_col

    @contact_info.setter
    def contact_info(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("contact_info must be a string.")
        v = value.strip()
        if len(v) < 7:
            raise ValueError("contact_info must be at least 7 characters.")
        self._contact_info_col = v

    def __repr__(self) -> str:
        return (
            f"<Tenant id={self.id} name='{self.name}' "
            f"contact='{self.contact_info}'>"
        )
