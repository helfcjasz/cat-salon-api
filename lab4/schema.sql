
CREATE TABLE IF NOT EXISTS cats (
    id    serial PRIMARY KEY,
    name  text NOT NULL CHECK (length(btrim(name)) > 0),
    breed text NOT NULL CHECK (length(btrim(breed)) > 0),
    UNIQUE (name, breed)
);

CREATE TABLE IF NOT EXISTS services (
    id           serial PRIMARY KEY,
    title        text NOT NULL UNIQUE,
    price        numeric(8, 2) NOT NULL CHECK (price >= 0),
    duration_min integer NOT NULL CHECK (duration_min > 0)
);

CREATE TABLE IF NOT EXISTS visits (
    id         serial PRIMARY KEY,
    cat_id     integer NOT NULL REFERENCES cats (id) ON DELETE CASCADE,
    visit_date date NOT NULL,
    cat_weight numeric(4, 1) NOT NULL CHECK (cat_weight BETWEEN 1 AND 20),
    confirmed  boolean NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS visit_services (
    visit_id   integer NOT NULL REFERENCES visits (id) ON DELETE CASCADE,
    service_id integer NOT NULL REFERENCES services (id),
    PRIMARY KEY (visit_id, service_id)
);