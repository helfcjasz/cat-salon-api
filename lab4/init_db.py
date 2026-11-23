import argparse
from datetime import date, time, timedelta
from pathlib import Path

import psycopg

from lab4.db import get_connection

SCHEMA_FILE = Path(__file__).with_name("schema.sql")

RESET_SQL = (
    "DROP TABLE IF EXISTS visit_services, visits, cats, services CASCADE"
)

SERVICES = [
    "Купання та сушіння",
    "Вичісування",
    "Гігієнічна стрижка",
    "Догляд за кігтиками та вушками",
    "Масаж лапок"
]


CATS = [
    ("Ніка", "сіамська кішка", 5.5, False),
    ("Мія", "метис", 3.4, True),
    ("Люся", "сибірська", 3.1, False),
    ("Йосип", "метис", 5.2, False),
    ("Марсік", "британський короткошерстий", 4.8, True),
    ("Боня", "метис", 3.1, False),
    ("Бідон", "мейн-кун", 10.2, False),
    ("Барсік", "мейнкун", 7.8, True),
    ("Петрик", "мейнкун", 8.4, False),
    ("Богдан", "сфінкс", 6.2, True),
    ("Леопольд", "мейнкун", 9.1, False),
    ("Гертруда", "мейнкун", 7.0, False),
    ("Боніфацій", "мейнкун", 8.8, False),
    ("Маркіза", "мейнкун", 5.9, True),
    ("Цезар", "мейнкун", 9.4, False),
    ("Гектор", "мейнкун", 8.1, True),
    ("Зефір", "мейнкун", 6.6, False),

]


def build_visits() -> list[tuple[int, date, time, list[str]]]:
    visits: list[tuple[int, date, time, list[str]]] = [
        (1, date(2026, 11, 25), time(10, 0), ["Вичісування"]),
        (2, date(2026, 11, 25), time(12, 0), ["Купання та сушіння"]),
        (3, date(2026, 11, 26), time(11, 0), ["Вичісування"]),
        (4, date(2026, 11, 26), time(14, 0), ["Догляд за кігтиками та вушками"]),
        (5, date(2026, 11, 27), time(15, 0), ["Гігієнічна стрижка"]),
    ]
    for number in range(6, 26):
        cat_index = (number - 1) % len(CATS)
        chosen = list(
            dict.fromkeys([SERVICES[number % len(SERVICES)], SERVICES[(number + 2) % len(SERVICES)]])
        )
        visit_hour = 10 + (number % 7)  
        visits.append(
            (
                cat_index + 1,
                date(2026, 11, 20) + timedelta(days=number),
                time(visit_hour, 0),
                chosen,
            )
        )
    return visits


def _insert(cur: psycopg.Cursor, sql: str, params: tuple) -> int:
    row = cur.execute(sql, params).fetchone()
    assert row is not None
    return int(row[0])


def seed(conn: psycopg.Connection) -> None:
    
    with conn.cursor() as cur:
        row = cur.execute("SELECT count(*) FROM visits").fetchone()
        if row is not None and row[0] > 0:
            print("Дані вже є, пропускаю вставку.")
            return

        service_ids = {
            name: _insert(
                cur,
                "INSERT INTO services (name) "
                "VALUES (%s) RETURNING id",
                (name,),
            )
            for name in SERVICES
        }
        cat_ids = [
            _insert(
                cur,
                "INSERT INTO cats (name, breed, weight, is_aggressive) VALUES (%s, %s, %s, %s) RETURNING id",
                (name, breed, weight, is_aggressive),
            )
            for name, breed, weight, is_aggressive in CATS
        ]
        for cat_number, service_date, service_time , names in build_visits():
            visit_id = _insert(
                cur,
                "INSERT INTO visits (cat_id, service_date, service_time) "
                "VALUES (%s, %s, %s) RETURNING id",
                (cat_ids[cat_number - 1], service_date, service_time),
            )
            cur.executemany(
                "INSERT INTO visit_services (visit_id, service_id) VALUES (%s, %s)",
                [(visit_id, service_ids[name]) for name in names],
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Ініціалізація БД салону")
    parser.add_argument(
        "--reset", action="store_true", help="видалити таблиці й створити ще раз"
    )
    args = parser.parse_args()

    with get_connection() as conn:
        if args.reset:
            conn.execute(RESET_SQL)
            print("Старі таблиці видалено.")
        conn.execute(SCHEMA_FILE.read_text(encoding="utf-8"))
        seed(conn)
        rows = conn.execute(
            "SELECT 'cats', count(*) FROM cats "
            "UNION ALL SELECT 'services', count(*) FROM services "
            "UNION ALL SELECT 'visits', count(*) FROM visits "
            "UNION ALL SELECT 'visit_services', count(*) FROM visit_services"
        ).fetchall()
    total = 0
    for table, count in rows:
        print(f"{table}: {count}")
        total += count
    print(f"Усього записів: {total}")


if __name__ == "__main__":
    main()