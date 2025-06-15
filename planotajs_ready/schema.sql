CREATE TABLE lietotaji (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lietotajvards TEXT,
    parole TEXT
);

CREATE TABLE uzdevumi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lietotajs_id INTEGER,
    nosaukums TEXT,
    termins TEXT,
    prioritate TEXT,
    FOREIGN KEY (lietotajs_id) REFERENCES lietotaji(id)
);
