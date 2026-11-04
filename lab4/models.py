from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


@dataclass
class Cat:
    id: int
    name: str
    breed: str


@dataclass
class Service:
    id: int
    title: str
    price: Decimal
    duration_min: int


@dataclass
class Visit:
    id: int
    cat: Cat
    visit_date: date
    cat_weight: Decimal
    confirmed: bool
    services: list[Service] = field(default_factory=list)


@dataclass(frozen=True)
class NewVisit:
    cat_name: str
    cat_breed: str
    services: list[str]
    visit_date: date
    cat_weight: Decimal
    confirmed: bool
