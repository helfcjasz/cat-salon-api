from typing import Protocol

from lab4.models import NewVisit, Visit


class ServiceNotFoundError(Exception):
    """Однієї чи кількох послуг немає в каталозі."""

    def __init__(self, titles: list[str]) -> None:
        super().__init__(", ".join(titles))
        self.titles = titles


class VisitRepository(Protocol):
    def list_all(self) -> list[Visit]: ...

    def get(self, visit_id: int) -> Visit | None: ...

    def create(self, data: NewVisit) -> Visit: ...

    def update(self, visit_id: int, data: NewVisit) -> Visit | None: ...

    def delete(self, visit_id: int) -> bool: ...
