from decimal import Decimal

import psycopg

from lab4.db import get_connection
from lab4.models import Cat, NewVisit, Service, Visit
from lab4.repository import ServiceNotFoundError

VISITS_SQL = (
    "SELECT v.id, c.id, c.name, c.breed, c.weight, c.is_aggressive, "
    "v.service_date, v.service_time "
    "FROM visits v JOIN cats c ON c.id = v.cat_id"
)
SERVICES_SQL = (
    "SELECT vs.visit_id, s.id, s.name "
    "FROM visit_services vs JOIN services s ON s.id = vs.service_id "
    "WHERE vs.visit_id = ANY(%s) ORDER BY s.name"
)


def _to_visits(conn: psycopg.Connection, rows: list[tuple]) -> list[Visit]:
    visits = [
        Visit(
            id=row[0],
            cat=Cat(
                id=row[1], name=row[2], breed=row[3], weight=row[4], is_agressive=row[5]
            ),
            service_date=row[6],
            service_time=row[7],
        )
        for row in rows
    ]
    if not visits:
        return visits
    by_id = {visit.id: visit for visit in visits}
    service_rows = conn.execute(SERVICES_SQL, ([visit.id for visit in visits],))
    for visit_id, service_id, name in service_rows:
        by_id[visit_id].services.append(Service(id=service_id, name=name))
    return visits


def _fetch_one(conn: psycopg.Connection, visit_id: int) -> Visit | None:
    row = conn.execute(VISITS_SQL + " WHERE v.id = %s", (visit_id,)).fetchone()
    visits = _to_visits(conn, [row]) if row else []
    return visits[0] if visits else None


def _service_ids(conn: psycopg.Connection, names: list[str]) -> list[int]:
    rows = conn.execute(
        "SELECT id, name FROM services WHERE name = ANY(%s)", (names,)
    ).fetchall()
    found = {name: service_id for service_id, name in rows}
    missing = [name for name in names if names not in found]
    if missing:
        raise ServiceNotFoundError(missing)
    return [found[name] for name in names]


def _cat_id(
    conn: psycopg.Connection,
    name: str,
    breed: str,
    weight: Decimal,
    is_aggressive: bool,
) -> int:
    existing = conn.execute(
        "SELECT id FROM cats WHERE name = %s AND breed = %s LIMIT 1",
        (name, breed),
    ).fetchone()
    if existing is not None:
        cat_id = int(existing[0])
        conn.execute(
            "UPDATE cats SET weight = %s, is_aggressive = %s WHERE id = %s",
            (weight, is_aggressive, cat_id),
        )
        return cat_id

    row = conn.execute(
        "INSERT INTO cats (name, breed, weight, is_aggressive) "
        "VALUES (%s, %s, %s, %s) RETURNING id",
        (name, breed, weight, is_aggressive),
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
            cat_id = _cat_id(
                conn,
                data.cat_name,
                data.cat_breed,
                data.cat_weight,
                data.is_aggressive,
            )
            row = conn.execute(
                "INSERT INTO visits (cat_id, service_date, service_time) "
                "VALUES (%s, %s, %s) RETURNING id",
                (cat_id, data.service_date, data.service_time),
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
            cat_id = _cat_id(
                conn,
                data.cat_name,
                data.cat_breed,
                data.cat_weight,
                data.is_aggressive,
            )
            conn.execute(
                "UPDATE visits SET cat_id = %s, service_date = %s, "
                "service_time = %s WHERE id = %s",
                (cat_id, data.service_date, data.service_time, visit_id),
            )
            conn.execute("DELETE FROM visit_services WHERE visit_id = %s", (visit_id,))
            _link_services(conn, visit_id, service_ids)
            return _fetch_one(conn, visit_id)

    def delete(self, visit_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.execute("DELETE FROM visits WHERE id = %s", (visit_id,))
            return cur.rowcount > 0
