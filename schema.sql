CREATE TABLE users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     TEXT PRIMARY KEY,            -- Unique identifier for the user (UUID)
    public_key  TEXT NOT NULL,               -- PEM-encoded key
    fingerprint TEXT UNIQUE NOT NULL,        -- SHA-256 of the key
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_users_user_id ON users(user_id);
CREATE INDEX idx_users_fingerprint ON users(fingerprint);

-- Auto-update updated_at on users
CREATE TRIGGER update_users_updated_at
    AFTER UPDATE ON users
    BEGIN
        UPDATE users SET updated_at = datetime('now') WHERE id = NEW.id;
    END;

PRAGMA foreign_keys = ON;