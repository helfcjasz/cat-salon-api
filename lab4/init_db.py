import argparse
from datetime import date, timedelta
from pathlib import Path

import psycopg

from lab4.db import get_connection

SCHEMA_FILE = Path(__file__).with_name("schema.sql")

RESET_SQL = (
    "DROP TABLE IF EXISTS visit_services, visits, cats, "
    "groomers, owners, services CASCADE"
)


SERVICES = [
    ("Купання та сушіння", 450, 50),
    ("Вичісування", 350, 40),
    ("Гігієнічна стрижка", 600, 60),
    ("Догляд за кігтиками та вушками", 250, 30),
    ("Видалення ковтунів", 400, 45),
    ("SPA-догляд за шерстю", 700, 75),
]

CATS = [
    ("Ніка", "сіамська кішка", 5.5),
    ("Мія", "метис", 3.4),
    ("Люся", "сибірська", 3.1),
    ("Йосип", "метис", 5.2),
    ("Марсік", "британський короткошерстий", 4.8),
    ("Барсик", "мейнкун", 7.8),
    ("Симба", "мейнкун", 8.4),
    ("Багіра", "мейнкун", 6.2),
    ("Леопольд", "мейнкун", 9.1),
    ("Рижик", "мейнкун", 7.0),
    ("Боніфацій", "мейнкун", 8.8),
    ("Маркіза", "мейнкун", 5.9),
    ("Цезар", "мейнкун", 9.4),
    ("Гектор", "мейнкун", 8.1),
    ("Зефір", "мейнкун", 6.6),
]


def build_visits() -> list[tuple[int, date, float, bool, list[str]]]:

    titles = [title for title, _, _ in SERVICES]
    visits = [
        # Перші п'ять візитів із server.js сайту.
        (1, date(2026, 11, 6), 5.5, False, ["Вичісування"]),
        (2, date(2026, 11, 3), 3.4, True, ["Купання та сушіння"]),
        (3, date(2026, 11, 1), 3.1, True, ["Вичісування"]),
        (4, date(2026, 11, 5), 5.2, True, ["Догляд за кігтиками та вушками"]),
        (5, date(2026, 11, 20), 4.8, True, ["Гігієнічна стрижка"]),
    ]
    for number in range(6, 26):
        cat_index = (number - 1) % len(CATS)
        chosen = list(dict.fromkeys([titles[number % 6], titles[(number * 5) % 6]]))
        visits.append(
            (
                cat_index + 1,
                date(2026, 10, 1) + timedelta(days=3 * number),
                CATS[cat_index][2],
                number % 3 != 0,
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
            title: _insert(
                cur,
                "INSERT INTO services (title, price, duration_min) "
                "VALUES (%s, %s, %s) RETURNING id",
                (title, price, minutes),
            )
            for title, price, minutes in SERVICES
        }
        cat_ids = [
            _insert(
                cur,
                "INSERT INTO cats (name, breed) VALUES (%s, %s) RETURNING id",
                (name, breed),
            )
            for name, breed, _ in CATS
        ]
        for cat_number, visit_date, weight, confirmed, titles in build_visits():
            visit_id = _insert(
                cur,
                "INSERT INTO visits (cat_id, visit_date, cat_weight, confirmed) "
                "VALUES (%s, %s, %s, %s) RETURNING id",
                (cat_ids[cat_number - 1], visit_date, weight, confirmed),
            )
            cur.executemany(
                "INSERT INTO visit_services (visit_id, service_id) VALUES (%s, %s)",
                [(visit_id, service_ids[title]) for title in titles],
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Ініціалізація БД салону")
    parser.add_argument(
        "--reset", action="store_true", help="видалити таблиці й створити заново"
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
