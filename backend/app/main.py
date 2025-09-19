from __future__ import annotations

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import SessionLocal, get_db, init_db
from .models import PersonalStatusType

app = FastAPI(title="Employee Personal Status API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    with SessionLocal() as session:
        crud.ensure_seed_data(session)
        session.commit()


def serialize_employee(employee) -> schemas.EmployeeRead:
    statuses = sorted(
        employee.statuses,
        key=lambda item: item.status_start or item.created_at,
        reverse=True,
    )
    current_status = None
    for status in statuses:
        if status.status_end is None:
            current_status = status
            break
    if current_status is None and statuses:
        current_status = statuses[0]

    return schemas.EmployeeRead(
        emp_id=employee.emp_id,
        emp_no=employee.emp_no,
        name=employee.name,
        email=employee.email,
        mobile=employee.mobile,
        department_name=employee.department.dept_name if employee.department else None,
        role_name=employee.role.role_name if employee.role else None,
        password_hash=employee.member.password_hash if employee.member else None,
        current_status=(
            schemas.PersonalStatusRead.model_validate(current_status)
            if current_status
            else None
        ),
    )


def serialize_member(member) -> schemas.MemberProfileRead:
    employee_data = serialize_employee(member.employee) if member.employee else None
    return schemas.MemberProfileRead(
        member_id=member.member_id,
        login_id=member.login_id,
        user_type=member.user_type,
        employee=employee_data,
    )


@app.get("/employees", response_model=List[schemas.EmployeeRead])
def get_employees(db: Session = Depends(get_db)) -> List[schemas.EmployeeRead]:
    employees = crud.list_employees(db)
    return [serialize_employee(employee) for employee in employees]


@app.put("/employees/{emp_id}", response_model=schemas.EmployeeRead)
def update_employee(emp_id: int, payload: schemas.EmployeeUpdate, db: Session = Depends(get_db)) -> schemas.EmployeeRead:
    employee = crud.update_employee(
        db,
        emp_id,
        name=payload.name,
        email=payload.email,
        mobile=payload.mobile,
        password_hash=payload.password_hash,
    )
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.refresh(employee)
    return serialize_employee(employee)


@app.put("/employees/{emp_id}/status", response_model=schemas.PersonalStatusRead)
def update_status(
    emp_id: int,
    payload: schemas.StatusUpdate,
    db: Session = Depends(get_db),
) -> schemas.PersonalStatusRead:
    status = crud.set_personal_status(db, emp_id, status=payload.status, note=payload.note)
    if status is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.refresh(status)
    return schemas.PersonalStatusRead.model_validate(status)


@app.get("/status-options", response_model=List[PersonalStatusType])
def get_status_options() -> List[PersonalStatusType]:
    return list(PersonalStatusType)


@app.get("/members/{login_id}", response_model=schemas.MemberProfileRead)
def get_member_profile(login_id: str, db: Session = Depends(get_db)) -> schemas.MemberProfileRead:
    member = crud.get_member_by_login_id(db, login_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    return serialize_member(member)


@app.put("/members/{login_id}", response_model=schemas.MemberProfileRead)
def update_member_profile(
    login_id: str,
    payload: schemas.MemberProfileUpdate,
    db: Session = Depends(get_db),
) -> schemas.MemberProfileRead:
    member = crud.update_member_profile(
        db,
        login_id,
        name=payload.name,
        email=payload.email,
        mobile=payload.mobile,
        password_hash=payload.password_hash,
    )
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found or employee not linked")

    return serialize_member(member)


@app.put("/members/{login_id}/status", response_model=schemas.PersonalStatusRead)
def update_member_status(
    login_id: str,
    payload: schemas.StatusUpdate,
    db: Session = Depends(get_db),
) -> schemas.PersonalStatusRead:
    status = crud.set_member_status(db, login_id, status=payload.status, note=payload.note)
    if status is None:
        raise HTTPException(status_code=404, detail="Member not found or employee not linked")

    db.refresh(status)
    return schemas.PersonalStatusRead.model_validate(status)
