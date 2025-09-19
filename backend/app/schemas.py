from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from .models import PersonalStatusType


class PersonalStatusRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status_id: int
    status: PersonalStatusType
    status_start: datetime
    status_end: Optional[datetime]
    note: Optional[str]


class EmployeeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    emp_id: int
    emp_no: str
    name: str
    email: EmailStr
    mobile: str
    department_name: Optional[str]
    role_name: Optional[str]
    password_hash: Optional[str]
    current_status: Optional[PersonalStatusRead]


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = None
    password_hash: Optional[str] = None


class StatusUpdate(BaseModel):
    status: PersonalStatusType
    note: Optional[str] = None


class MemberProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    member_id: int
    login_id: str
    user_type: str
    employee: Optional[EmployeeRead]


class MemberProfileUpdate(EmployeeUpdate):
    pass
