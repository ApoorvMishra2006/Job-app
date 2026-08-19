import hashlib
import hmac
import os

from utils.logger import logger


def hash_password(password):

    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100000
    )

    return (
        salt.hex(),
        password_hash.hex()
    )


def verify_password(password, salt, stored_hash):

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        bytes.fromhex(salt),
        100000
    )

    return hmac.compare_digest(
        password_hash.hex(),
        stored_hash
    )


def validate_password(password):

    if len(password) < 8:

        return False

    return True


def register_user(
    connection,
    username,
    email,
    password
):

    if not username.strip():

        return False, "Username cannot be empty."

    if not email.strip():

        return False, "Email cannot be empty."

    if not validate_password(password):

        return False, (
            "Password must be at least 8 characters."
        )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        OR email = ?
        """,
        (
            username.strip(),
            email.strip().lower()
        )
    )

    existing_user = cursor.fetchone()

    if existing_user:

        return False, (
            "Username or email already exists."
        )

    salt, password_hash = hash_password(password)

    cursor.execute(
        """
        INSERT INTO users (
            username,
            email,
            password_hash,
            password_salt
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            username.strip(),
            email.strip().lower(),
            password_hash,
            salt
        )
    )

    connection.commit()

    logger.info(
        f"New user registered: '{username.strip()}'"
    )

    return True, "Account created successfully."


def login_user(
    connection,
    username,
    password
):

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            username,
            email,
            password_hash,
            password_salt
        FROM users
        WHERE username = ?
        """,
        (username.strip(),)
    )

    user = cursor.fetchone()

    if not user:

        logger.info(
            f"Failed login attempt for username "
            f"'{username}'"
        )

        return None

    user_id = user[0]
    stored_username = user[1]
    email = user[2]
    password_hash = user[3]
    salt = user[4]

    if not verify_password(
        password,
        salt,
        password_hash
    ):

        logger.info(
            f"Failed login attempt for username "
            f"'{username}'"
        )

        return None

    logger.info(
        f"User logged in: '{stored_username}'"
    )

    return {
        "id": user_id,
        "username": stored_username,
        "email": email
    }