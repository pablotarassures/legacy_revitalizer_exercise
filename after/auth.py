import hmac

MAX_LOGIN_ATTEMPTS = 3


class AuthService:
    """
    Verifies user credentials. Credentials injected — not hardcoded.

    Design note — what this is NOT:
      - Passwords are compared in plaintext. In production, stored passwords
        should be hashed with bcrypt or argon2 (salt + slow hash). Never store
        or compare raw passwords against a database.
      - Credentials still come from environment variables, which are readable
        by any process in the same environment and can appear in crash dumps.
        In production, use a secrets manager (AWS Secrets Manager, HashiCorp
        Vault, etc.) and inject secrets at runtime, not at boot.
    """

    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password
        self._attempts = 0

    def authenticate(self, username: str, password: str) -> bool:
        """
        Timing-safe comparison via hmac.compare_digest().

        Plain == comparison leaks information: Python short-circuits on the
        first mismatched character, so an attacker measuring response time can
        infer how many characters of the password are correct. compare_digest()
        always takes the same time regardless of where the mismatch occurs.
        """
        if self._attempts >= MAX_LOGIN_ATTEMPTS:
            print("Too many failed attempts. Access locked.")
            return False

        username_match = hmac.compare_digest(username, self._username)
        password_match = hmac.compare_digest(password, self._password)

        if username_match and password_match:
            self._attempts = 0
            return True

        self._attempts += 1
        remaining = MAX_LOGIN_ATTEMPTS - self._attempts
        if remaining > 0:
            print(f"Wrong! {remaining} attempt(s) remaining.")
        return False

    @property
    def is_locked(self) -> bool:
        return self._attempts >= MAX_LOGIN_ATTEMPTS
