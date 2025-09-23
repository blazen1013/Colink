from datetime import datetime
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, schemas
from .config import get_settings
from .database import engine, get_db
from .models import Base, EmployeeStatusEnum

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _latest_status(employee) -> Optional[schemas.EmployeeStatusResponse]:
    if not employee.statuses:
        return None
    status_record = max(
        employee.statuses,
        key=lambda s: s.updated_at or datetime.min,
    )
    return schemas.EmployeeStatusResponse.from_orm(status_record)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/employees", response_model=list[schemas.EmployeeResponse])
def read_employees(db: Session = Depends(get_db)):
    employees = crud.list_employees(db)
    response = []
    for employee in employees:
        response.append(
            schemas.EmployeeResponse(
                emp_id=employee.emp_id,
                emp_no=employee.emp_no,
                dept_id=employee.dept_id,
                role_id=employee.role_id,
                name=employee.name,
                email=employee.email,
                mobile=employee.mobile,
                status=_latest_status(employee),
            )
        )
    return response


@app.put("/employees/{emp_id}", response_model=schemas.EmployeeResponse)
def update_employee(emp_id: int, payload: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    try:
        employee = crud.update_employee_profile(
            db,
            emp_id,
            name=payload.name,
            email=payload.email,
            mobile=payload.mobile,
            status=payload.status,
            password=payload.password,
        )
    except crud.EmployeeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except crud.MemberNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    return schemas.EmployeeResponse(
        emp_id=employee.emp_id,
        emp_no=employee.emp_no,
        dept_id=employee.dept_id,
        role_id=employee.role_id,
        name=employee.name,
        email=employee.email,
        mobile=employee.mobile,
        status=_latest_status(employee),
    )


@app.get("/employee-status-options")
def get_status_options():
    return {"options": [status.value for status in EmployeeStatusEnum]}
