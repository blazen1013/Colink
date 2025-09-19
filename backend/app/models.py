from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import (
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class PersonalStatusType(str, enum.Enum):
    WORKING = "WORKING"
    AWAY = "AWAY"
    OUT_ON_BUSINESS = "OUT_ON_BUSINESS"
    OFF_DUTY = "OFF_DUTY"


class Department(Base):
    __tablename__ = "department"

    dept_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    dept_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    employees: Mapped[list["Employee"]] = relationship("Employee", back_populates="department")


class Role(Base):
    __tablename__ = "role"

    role_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    role_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    role_level: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    employees: Mapped[list["Employee"]] = relationship("Employee", back_populates="role")


class Employee(Base):
    __tablename__ = "employee"

    emp_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    emp_no: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    dept_id: Mapped[int] = mapped_column(ForeignKey("department.dept_id"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.role_id"), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    mobile: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    hire_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    birthday: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    department: Mapped[Department] = relationship("Department", back_populates="employees")
    role: Mapped[Role] = relationship("Role", back_populates="employees")
    member: Mapped["Member"] = relationship(
        "Member", back_populates="employee", uselist=False, cascade="all, delete-orphan"
    )
    statuses: Mapped[list["PersonalStatus"]] = relationship(
        "PersonalStatus", back_populates="employee", cascade="all, delete-orphan"
    )


class Member(Base):
    __tablename__ = "member"
    __table_args__ = (
        UniqueConstraint("login_id"),
    )

    member_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    login_id: Mapped[str] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    emp_id: Mapped[int | None] = mapped_column(ForeignKey("employee.emp_id"), nullable=True)
    ext_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    user_type: Mapped[str] = mapped_column(String(20), nullable=False, default="EMPLOYEE")
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    failed_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    employee: Mapped[Employee | None] = relationship("Employee", back_populates="member")


class PersonalStatus(Base):
    __tablename__ = "personal_status"

    status_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    emp_id: Mapped[int] = mapped_column(ForeignKey("employee.emp_id"), nullable=False)
    status: Mapped[PersonalStatusType] = mapped_column(Enum(PersonalStatusType), nullable=False)
    status_start: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status_end: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    employee: Mapped[Employee] = relationship("Employee", back_populates="statuses")
