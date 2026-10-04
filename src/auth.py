import sqlite3
import hashlib
import hmac
import secrets
from pathlib import Path


DB_PATH = Path("data/users.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


def hash_password(password):
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200_000
    )

    return salt.hex(), password_hash.hex()


def verify_password(password, salt_hex, stored_hash):
    salt = bytes.fromhex(salt_hex)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200_000
    ).hex()

    return hmac.compare_digest(password_hash, stored_hash)


def create_user(full_name, email, password):

    full_name = full_name.strip()
    email = email.strip().lower()

    if not full_name:
        return False, "Full name is required."

    if not email:
        return False, "Email is required."

    if len(password) < 6:
        return False, "Password must contain at least 6 characters."

    salt, password_hash = hash_password(password)

    try:
        conn = get_connection()

        conn.execute(
            """
            INSERT INTO users
            (full_name, email, password_hash, salt)
            VALUES (?, ?, ?, ?)
            """,
            (full_name, email, password_hash, salt)
        )

        conn.commit()
        conn.close()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."


def authenticate_user(email, password):

    email = email.strip().lower()

    conn = get_connection()

    user = conn.execute(
        """
        SELECT id, full_name, email, password_hash, salt
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    conn.close()

    if user is None:
        return None

    user_id, full_name, email, stored_hash, salt = user

    if verify_password(password, salt, stored_hash):
        return {
            "id": user_id,
            "full_name": full_name,
            "email": email
        }

    return None