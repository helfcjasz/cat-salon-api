from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


@dataclass
class Service:
    id: int
    title: str
    price: Decimal
    duration_min: int


@dataclass
class Groomer:
    id: int
    full_name: str
    phone: str


@dataclass
class Cat:
    id: int
    owner_id: int
    name: str
    breed: str
    birth_date: date
    weight: Decimal


@dataclass
class Owner:
    id: int
    full_name: str
    email: str
    phone: str
    cats: list[Cat] = field(default_factory=list)


@dataclass
class Visit:
    id: int
    cat_id: int
    groomer_id: int
    visit_date: date
    status: str = "planned"
    services: list[Service] = field(default_factory=list)
