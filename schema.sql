-- Schema of the SQLite database we use to store the LBS price index data
BEGIN TRANSACTION;

CREATE TABLE series (
    area_code TEXT,
    item_code TEXT,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    index_value REAL,
    UNIQUE(area_code, item_code, year, month),
    FOREIGN KEY (area_code) REFERENCES areas (code),
    FOREIGN KEY (item_code) REFERENCES items (code)
);

CREATE TABLE areas (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE items (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

COMMIT;
