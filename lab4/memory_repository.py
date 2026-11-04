from lab4.models import Cat, NewVisit, Service, Visit
from lab4.repository import ServiceNotFoundError


class InMemoryVisitRepository:
    def __init__(self, services: list[Service]) -> None:
        self._services = {service.title: service for service in services}
        self._cats: dict[tuple[str, str], Cat] = {}
        self._visits: dict[int, Visit] = {}
        self._next_cat_id = 1
        self._next_visit_id = 1

    def _resolve_services(self, titles: list[str]) -> list[Service]:
        missing = [title for title in titles if title not in self._services]
        if missing:
            raise ServiceNotFoundError(missing)
        return sorted((self._services[title] for title in titles), key=_by_title)

    def _find_or_create_cat(self, name: str, breed: str) -> Cat:
        key = (name, breed)
        if key not in self._cats:
            self._cats[key] = Cat(self._next_cat_id, name, breed)
            self._next_cat_id += 1
        return self._cats[key]

    def list_all(self) -> list[Visit]:
        return [self._visits[visit_id] for visit_id in sorted(self._visits)]

    def get(self, visit_id: int) -> Visit | None:
        return self._visits.get(visit_id)

    def create(self, data: NewVisit) -> Visit:
        services = self._resolve_services(data.services)
        cat = self._find_or_create_cat(data.cat_name, data.cat_breed)
        visit = Visit(
            id=self._next_visit_id,
            cat=cat,
            visit_date=data.visit_date,
            cat_weight=data.cat_weight,
            confirmed=data.confirmed,
            services=services,
        )
        self._visits[visit.id] = visit
        self._next_visit_id += 1
        return visit

    def update(self, visit_id: int, data: NewVisit) -> Visit | None:
        if visit_id not in self._visits:
            return None
        services = self._resolve_services(data.services)
        visit = Visit(
            id=visit_id,
            cat=self._find_or_create_cat(data.cat_name, data.cat_breed),
            visit_date=data.visit_date,
            cat_weight=data.cat_weight,
            confirmed=data.confirmed,
            services=services,
        )
        self._visits[visit_id] = visit
        return visit

    def delete(self, visit_id: int) -> bool:
        return self._visits.pop(visit_id, None) is not None


def _by_title(service: Service) -> str:
    return service.title
