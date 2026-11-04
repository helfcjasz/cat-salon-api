from datetime import date
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
    catMass: float = Field(ge=1, le=20)
    confirmation: bool = False

    def to_new_visit(self) -> NewVisit:
        parts = (part.strip() for part in self.serviceType.split(","))
        titles = list(dict.fromkeys(part for part in parts if part))
        return NewVisit(
            cat_name=self.catName.strip(),
            cat_breed=self.catBreed.strip(),
            services=titles,
            visit_date=self.serviceDate,
            cat_weight=Decimal(str(self.catMass)),
            confirmed=self.confirmation,
        )


class ItemOut(BaseModel):
    id: int
    catName: str
    catBreed: str
    serviceType: str
    serviceDate: date
    catMass: float
    confirmation: bool

    @classmethod
    def from_visit(cls, visit: Visit) -> ItemOut:
        return cls(
            id=visit.id,
            catName=visit.cat.name,
            catBreed=visit.cat.breed,
            serviceType=", ".join(service.title for service in visit.services),
            serviceDate=visit.visit_date,
            catMass=float(visit.cat_weight),
            confirmation=visit.confirmed,
        )
