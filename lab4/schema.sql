CREATE TABLE IF NOT EXISTS owners (
    id        serial PRIMARY KEY,
    full_name text NOT NULL,
    email     text NOT NULL UNIQUE
              CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    phone     text NOT NULL UNIQUE
              CHECK (phone ~ '^\+380[0-9]{9}$')
);
 
CREATE TABLE IF NOT EXISTS cats (
    id         serial PRIMARY KEY,
    owner_id   integer NOT NULL REFERENCES owners (id) ON DELETE CASCADE,
    name       text NOT NULL,
    breed      text NOT NULL,
    birth_date date NOT NULL,
    weight     numeric(5, 1) NOT NULL CHECK (weight > 0 AND weight <= 100)
);
 
CREATE TABLE IF NOT EXISTS groomers (
    id        serial PRIMARY KEY,
    full_name text NOT NULL,
    phone     text NOT NULL UNIQUE
              CHECK (phone ~ '^\+380[0-9]{9}$')
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
    groomer_id integer NOT NULL REFERENCES groomers (id),
    visit_date date NOT NULL,
    status     text NOT NULL DEFAULT 'planned'
               CHECK (status IN ('planned', 'done', 'cancelled'))
);
 

CREATE TABLE IF NOT EXISTS visit_services (
    visit_id   integer NOT NULL REFERENCES visits (id) ON DELETE CASCADE,
    service_id integer NOT NULL REFERENCES services (id),
    PRIMARY KEY (visit_id, service_id)
);