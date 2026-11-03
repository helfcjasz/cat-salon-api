from datetime import date, timedelta
from pathlib import Path

import psycopg

from lab4.db import get_connection

SCHEMA_FILE = Path(__file__).with_name("schema.sql")

OWNERS = [
    ("Олена Коваленко", "olena.kovalenko@example.com", "+380501110001"),
    ("Андрій Мельник", "andrii.melnyk@example.com", "+380501110002"),
    ("Ірина Шевченко", "iryna.shevchenko@example.com", "+380501110003"),
    ("Тарас Бондаренко", "taras.bondarenko@example.com", "+380501110004"),
    ("Марія Ткаченко", "maria.tkachenko@example.com", "+380501110005"),
    ("Остап Кравченко", "ostap.kravchenko@example.com", "+380501110006"),
    ("Наталія Олійник", "natalia.oliinyk@example.com", "+380501110007"),
    ("Богдан Лисенко", "bohdan.lysenko@example.com", "+380501110008"),
    ("Соломія Гриценко", "solomiia.hrytsenko@example.com", "+380501110009"),
    ("Юрій Савчук", "yurii.savchuk@example.com", "+380501110010"),
]

GROOMERS = [
    ("Віктор Петренко", "+380672220001"),
    ("Оксана Мороз", "+380672220002"),
    ("Дмитро Руденко", "+380672220003"),
    ("Катерина Литвин", "+380672220004"),
]

SERVICES = [
    ("Гігієнічна стрижка", 600, 60),
    ("Повне миття та сушіння", 450, 50),
    ("Вичісування шерсті", 350, 40),
    ("Стрижка кігтів", 150, 15),
    ("Чистка вух", 120, 15),
    ("Видалення ковтунів", 400, 45),
    ("Грумінг мейнкуна (повний)", 900, 120),
    ("SPA-догляд за шерстю", 700, 75),
]

CAT_NAMES = [
    "Барсик", "Мурка", "Симба", "Багіра", "Леопольд",
    "Ліза", "Том", "Рижик", "Боніфацій", "Маркіза",
    "Філя", "Цезар", "Сніжинка", "Гектор", "Мотя",
    "Персик", "Тигран", "Ківі", "Оскар", "Зефір",
]  # fmt: skip


def seed(conn: psycopg.Connection) -> None:
    """Вставляє тестові дані, якщо таблиці порожні."""
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM owners")
        row = cur.fetchone()
        if row is not None and row[0] > 0:
            print("Дані вже є, пропускаю вставку.")
            return

        cur.executemany(
            "INSERT INTO owners (full_name, email, phone) VALUES (%s, %s, %s)",
            OWNERS,
        )
        cur.executemany(
            "INSERT INTO groomers (full_name, phone) VALUES (%s, %s)",
            GROOMERS,
        )
        cur.executemany(
            "INSERT INTO services (title, price, duration_min) VALUES (%s, %s, %s)",
            SERVICES,
        )

        cats = [
            (
                i // 2 + 1,
                name,
                "Британська короткошерста" if i % 5 == 4 else "Мейнкун",
                date(2018 + i % 7, 1 + i % 12, 1 + (i * 3) % 28),
                round(4.0 + (i % 10) * 0.6, 1),
            )
            for i, name in enumerate(CAT_NAMES)
        ]
        cur.executemany(
            "INSERT INTO cats (owner_id, name, breed, birth_date, weight) "
            "VALUES (%s, %s, %s, %s, %s)",
            cats,
        )

        visits = [
            (
                (v - 1) % 20 + 1,
                (v - 1) % 4 + 1,
                date(2026, 9, 1) + timedelta(days=3 * v),
                "done" if v <= 18 else "planned" if v <= 22 else "cancelled",
            )
            for v in range(1, 26)
        ]
        cur.executemany(
            "INSERT INTO visits (cat_id, groomer_id, visit_date, status) "
            "VALUES (%s, %s, %s, %s)",
            visits,
        )

        visit_services = sorted(
            {(v, s) for v in range(1, 26) for s in (v % 8 + 1, (3 * v) % 8 + 1)}
        )
        cur.executemany(
            "INSERT INTO visit_services (visit_id, service_id) VALUES (%s, %s)",
            visit_services,
        )


def main() -> None:
    with get_connection() as conn:
        conn.execute(SCHEMA_FILE.read_text(encoding="utf-8"))
        seed(conn)
        rows = conn.execute(
            "SELECT 'owners', count(*) FROM owners "
            "UNION ALL SELECT 'cats', count(*) FROM cats "
            "UNION ALL SELECT 'groomers', count(*) FROM groomers "
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
