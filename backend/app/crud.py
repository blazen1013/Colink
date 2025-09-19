from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from . import models


def list_employees(db: Session) -> list[models.Employee]:
    statement = (
        select(models.Employee)
        .options(
            joinedload(models.Employee.department),
            joinedload(models.Employee.role),
            joinedload(models.Employee.member),
            joinedload(models.Employee.statuses),
        )
        .order_by(models.Employee.emp_id)
    )
    result = db.execute(statement)
    return result.scalars().unique().all()


def update_employee(
    db: Session,
    emp_id: int,
    *,
    name: Optional[str] = None,
    email: Optional[str] = None,
    mobile: Optional[str] = None,
    password_hash: Optional[str] = None,
) -> Optional[models.Employee]:
    employee = db.get(models.Employee, emp_id)
    if employee is None:
        return None

    if name is not None:
        employee.name = name
    if email is not None:
        employee.email = email
    if mobile is not None:
        employee.mobile = mobile

    if password_hash is not None:
        if employee.member is None:
            employee.member = models.Member(
                login_id=employee.emp_no,
                user_type="EMPLOYEE",
                password_hash=password_hash,
            )
        else:
            employee.member.password_hash = password_hash

    db.add(employee)
    db.flush()
    return employee


def set_personal_status(
    db: Session,
    emp_id: int,
    *,
    status: models.PersonalStatusType,
    note: Optional[str] = None,
) -> Optional[models.PersonalStatus]:
    employee = db.get(models.Employee, emp_id)
    if employee is None:
        return None

    now = datetime.utcnow()

    current_status_stmt = (
        select(models.PersonalStatus)
        .where(models.PersonalStatus.emp_id == emp_id, models.PersonalStatus.status_end.is_(None))
        .order_by(models.PersonalStatus.status_start.desc())
    )
    current_status = db.execute(current_status_stmt).scalars().first()
    if current_status is not None:
        current_status.status_end = now

    new_status = models.PersonalStatus(
        emp_id=emp_id,
        status=status,
        status_start=now,
        note=note,
    )
    db.add(new_status)
    db.flush()
    return new_status


def get_member_by_login_id(db: Session, login_id: str) -> models.Member | None:
    statement = (
        select(models.Member)
        .options(
            joinedload(models.Member.employee)
            .joinedload(models.Employee.department),
            joinedload(models.Member.employee)
            .joinedload(models.Employee.role),
            joinedload(models.Member.employee)
            .joinedload(models.Employee.statuses),
        )
        .where(models.Member.login_id == login_id)
    )
    return db.execute(statement).scalars().first()


def update_member_profile(
    db: Session,
    login_id: str,
    *,
    name: Optional[str] = None,
    email: Optional[str] = None,
    mobile: Optional[str] = None,
    password_hash: Optional[str] = None,
) -> models.Member | None:
    member = get_member_by_login_id(db, login_id)
    if member is None or member.employee is None:
        return None

    update_employee(
        db,
        member.employee.emp_id,
        name=name,
        email=email,
        mobile=mobile,
        password_hash=password_hash,
    )
    db.flush()
    return get_member_by_login_id(db, login_id)


def set_member_status(
    db: Session,
    login_id: str,
    *,
    status: models.PersonalStatusType,
    note: Optional[str] = None,
) -> models.PersonalStatus | None:
    member = get_member_by_login_id(db, login_id)
    if member is None or member.employee is None:
        return None

    return set_personal_status(db, member.employee.emp_id, status=status, note=note)


def ensure_seed_data(db: Session) -> None:
    if db.execute(select(models.Department)).first() is None:
        departments = [
            models.Department(dept_name="경영지원팀"),
            models.Department(dept_name="개발팀"),
        ]
        db.add_all(departments)

    if db.execute(select(models.Role)).first() is None:
        roles = [
            models.Role(role_name="사원", role_level=1),
            models.Role(role_name="팀장", role_level=2),
        ]
        db.add_all(roles)

    if db.execute(select(models.Employee)).first() is None:
        default_dept = db.execute(select(models.Department).order_by(models.Department.dept_id)).scalars().first()
        default_role = db.execute(select(models.Role).order_by(models.Role.role_id)).scalars().first()
        if default_dept is None or default_role is None:
            db.flush()
            default_dept = db.execute(select(models.Department).order_by(models.Department.dept_id)).scalars().first()
            default_role = db.execute(select(models.Role).order_by(models.Role.role_id)).scalars().first()

        employees = [
            models.Employee(
                emp_no="D001001",
                dept_id=default_dept.dept_id,
                role_id=default_role.role_id,
                name="김철수",
                email="kim@example.com",
                mobile="010-1111-2222",
            ),
            models.Employee(
                emp_no="D001002",
                dept_id=default_dept.dept_id,
                role_id=default_role.role_id,
                name="이영희",
                email="lee@example.com",
                mobile="010-3333-4444",
            ),
        ]
        db.add_all(employees)
        db.flush()

        for employee in employees:
            employee.member = models.Member(
                login_id=employee.emp_no,
                password_hash="changeme",
                user_type="EMPLOYEE",
            )
            employee.statuses.append(
                models.PersonalStatus(status=models.PersonalStatusType.WORKING)
            )
    db.flush()
