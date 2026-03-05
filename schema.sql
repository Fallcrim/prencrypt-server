CREATE TABLE users (
    user_id     TEXT PRIMARY KEY,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE user_public_keys (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    public_key  TEXT NOT NULL,               -- PEM-encoded key
    fingerprint TEXT UNIQUE NOT NULL,        -- SHA-256 of the key
    is_active   INTEGER NOT NULL DEFAULT 1,  -- SQLite has no BOOLEAN, use 0/1
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    revoked_at  TEXT                         -- NULL = active
);

CREATE INDEX idx_user_public_keys_user_id ON user_public_keys(user_id);
CREATE INDEX idx_user_public_keys_fingerprint ON user_public_keys(fingerprint);

-- Auto-update updated_at on users
CREATE TRIGGER update_users_updated_at
    AFTER UPDATE ON users
    BEGIN
        UPDATE users SET updated_at = datetime('now') WHERE id = NEW.id;
    END;

-- Enable foreign key enforcement (off by default in SQLite!)
PRAGMA foreign_keys = ON;