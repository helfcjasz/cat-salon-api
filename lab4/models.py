from dataclasses import dataclass, field
from datetime import date, time
from decimal import Decimal


@dataclass
class Cat:
    id: int
    name: str
    breed: str
    weight: Decimal
    is_agressive: bool = False


@dataclass
class Service:
    id: int
    name: str


@dataclass
class Visit:
    id: int
    cat: Cat
    service_date: date
    service_time: time
    services: list[Service] = field(default_factory=list)


@dataclass(frozen=True)
class NewVisit:
    cat_name: str
    cat_breed: str
    cat_weight: Decimal
    is_agressive: bool
    services: list[str]
    service_date: date
    service_time: time

