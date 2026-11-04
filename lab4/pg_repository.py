import psycopg

from lab4.db import get_connection
from lab4.models import Cat, NewVisit, Service, Visit
from lab4.repository import ServiceNotFoundError

VISITS_SQL = (
    "SELECT v.id, c.id, c.name, c.breed, v.visit_date, v.cat_weight, v.confirmed "
    "FROM visits v JOIN cats c ON c.id = v.cat_id"
)
SERVICES_SQL = (
    "SELECT vs.visit_id, s.id, s.title, s.price, s.duration_min "
    "FROM visit_services vs JOIN services s ON s.id = vs.service_id "
    "WHERE vs.visit_id = ANY(%s) ORDER BY s.title"
)


def _to_visits(conn: psycopg.Connection, rows: list[tuple]) -> list[Visit]:
    visits = [
        Visit(
            id=row[0],
            cat=Cat(id=row[1], name=row[2], breed=row[3]),
            visit_date=row[4],
            cat_weight=row[5],
            confirmed=row[6],
        )
        for row in rows
    ]
    if not visits:
        return visits
    by_id = {visit.id: visit for visit in visits}
    service_rows = conn.execute(SERVICES_SQL, ([visit.id for visit in visits],))
    for visit_id, service_id, title, price, minutes in service_rows:
        by_id[visit_id].services.append(Service(service_id, title, price, minutes))
    return visits


def _fetch_one(conn: psycopg.Connection, visit_id: int) -> Visit | None:
    row = conn.execute(VISITS_SQL + " WHERE v.id = %s", (visit_id,)).fetchone()
    visits = _to_visits(conn, [row]) if row else []
    return visits[0] if visits else None


def _service_ids(conn: psycopg.Connection, titles: list[str]) -> list[int]:
    rows = conn.execute(
        "SELECT id, title FROM services WHERE title = ANY(%s)", (titles,)
    ).fetchall()
    found = {title: service_id for service_id, title in rows}
    missing = [title for title in titles if title not in found]
    if missing:
        raise ServiceNotFoundError(missing)
    return [found[title] for title in titles]


def _cat_id(conn: psycopg.Connection, name: str, breed: str) -> int:
    """Знаходить кота за кличкою та породою або створює нового."""
    row = conn.execute(
        "INSERT INTO cats (name, breed) VALUES (%s, %s) "
        "ON CONFLICT (name, breed) DO UPDATE SET name = EXCLUDED.name "
        "RETURNING id",
        (name, breed),
    ).fetchone()
    assert row is not None
    return int(row[0])


def _link_services(
    conn: psycopg.Connection, visit_id: int, service_ids: list[int]
) -> None:
    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO visit_services (visit_id, service_id) VALUES (%s, %s)",
            [(visit_id, service_id) for service_id in service_ids],
        )


class PostgresVisitRepository:
    def list_all(self) -> list[Visit]:
        with get_connection() as conn:
            rows = conn.execute(VISITS_SQL + " ORDER BY v.id").fetchall()
            return _to_visits(conn, rows)

    def get(self, visit_id: int) -> Visit | None:
        with get_connection() as conn:
            return _fetch_one(conn, visit_id)

    def create(self, data: NewVisit) -> Visit:
        with get_connection() as conn:
            service_ids = _service_ids(conn, data.services)
            cat_id = _cat_id(conn, data.cat_name, data.cat_breed)
            row = conn.execute(
                "INSERT INTO visits (cat_id, visit_date, cat_weight, confirmed) "
                "VALUES (%s, %s, %s, %s) RETURNING id",
                (cat_id, data.visit_date, data.cat_weight, data.confirmed),
            ).fetchone()
            assert row is not None
            visit_id = int(row[0])
            _link_services(conn, visit_id, service_ids)
            visit = _fetch_one(conn, visit_id)
            assert visit is not None
            return visit

    def update(self, visit_id: int, data: NewVisit) -> Visit | None:
        with get_connection() as conn:
            exists = conn.execute(
                "SELECT 1 FROM visits WHERE id = %s", (visit_id,)
            ).fetchone()
            if exists is None:
                return None
            service_ids = _service_ids(conn, data.services)
            cat_id = _cat_id(conn, data.cat_name, data.cat_breed)
            conn.execute(
                "UPDATE visits SET cat_id = %s, visit_date = %s, "
                "cat_weight = %s, confirmed = %s WHERE id = %s",
                (cat_id, data.visit_date, data.cat_weight, data.confirmed, visit_id),
            )
            conn.execute("DELETE FROM visit_services WHERE visit_id = %s", (visit_id,))
            _link_services(conn, visit_id, service_ids)
            return _fetch_one(conn, visit_id)

    def delete(self, visit_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.execute("DELETE FROM visits WHERE id = %s", (visit_id,))
            return cur.rowcount > 0
