from dataclasses import dataclass
from typing import Optional


@dataclass
class ApplicantInformation:
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    birth_date: Optional[str] = ""
    gender: Optional[str] = None
    phone: Optional[str] = ""
    email: Optional[str] = ""
    parent: Optional[str] = None
    tobacco: Optional[str] = None
    annual_income: Optional[str] = ""
    household_members: Optional[str] = ""


@dataclass
class SpouseInformation:
    birth_date: str = None
    gender: str = None
    tobacco: Optional[str] = None
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""


@dataclass
class DependentInformation:
    birth_date: str = None
    gender: str = None
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
