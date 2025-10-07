import hashlib


def hash_password(password):
    # TODO Static salt for simplicity (replace with dynamic salting for better security)
    salt = "static_salt_12345"
    """Hash the password with a static salt."""
    return hashlib.sha256((salt + password).encode()).hexdigest()
