from __future__ import annotations

from datetime import date, time
from decimal import Decimal

from pydantic import BaseModel, Field

from lab4.models import NewVisit, Visit

NAME_PATTERN = r"^[^\W\d_](?:[^\W\d_]|[' -]){0,49}$"
SERVICES_PATTERN = r"^[^\W\d_](?:[^\W\d_]|[ ,'-]){0,199}$"


class ItemIn(BaseModel):
    catName: str = Field(pattern=NAME_PATTERN)
    catBreed: str = Field(pattern=NAME_PATTERN)
    serviceType: str = Field(pattern=SERVICES_PATTERN)
    serviceDate: date
    serviceTime: time
    catMass: float = Field(ge=1, le=20)
    agr_confirmation: bool = False

    def to_new_visit(self) -> NewVisit:
        parts = (part.strip() for part in self.serviceType.split(","))
        names = list(dict.fromkeys(part for part in parts if part))
        return NewVisit(
            cat_name=self.catName.strip(),
            cat_breed=self.catBreed.strip(),
            cat_weight=Decimal(str(self.catMass)),
            is_aggressive=self.agr_confirmation,
            services=names,
            service_date=self.serviceDate,
            service_time=self.serviceTime,
        )


class ItemOut(BaseModel):
    id: int
    catName: str
    catBreed: str
    serviceType: str
    serviceDate: date
    serviceTime: str
    catMass: float
    agr_confirmation: bool

    @classmethod
    def from_visit(cls, visit: Visit) -> ItemOut:
        return cls(
            id=visit.id,
            catName=visit.cat.name,
            catBreed=visit.cat.breed,
            serviceType=", ".join(service.name for service in visit.services),
            serviceDate=visit.service_date,
            serviceTime=visit.service_time.strftime("%H:%M"),
            catMass=float(visit.cat.weight),
            agr_confirmation=visit.cat.is_agressive,
        )
