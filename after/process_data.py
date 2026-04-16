import os
import sys

from auth import AuthService
from repository import FileRepository
from store import DataStore


def _read_input(prompt: str) -> str:
    """Wraps input() to handle EOF from piped or redirected stdin."""
    try:
        return input(prompt)
    except EOFError:
        raise EOFError("Input stream closed unexpectedly.")


def _load_credentials() -> tuple[str, str]:
    """
    Load credentials from environment variables.

    Fails fast if either variable is missing rather than silently falling back
    to hardcoded defaults. Hardcoded fallbacks are a common cause of credentials
    being shipped to production unchanged — fail loudly so the misconfiguration
    is caught at startup, not discovered after a breach.

    Production upgrade path: replace os.environ with a call to a secrets
    manager SDK (e.g. boto3 for AWS Secrets Manager) so secrets are fetched
    at runtime and never written to disk or environment.
    """
    username = os.environ.get("APP_USERNAME")
    password = os.environ.get("APP_PASSWORD")

    if not username or not password:
        print(
            "Error: APP_USERNAME and APP_PASSWORD environment variables must be set.\n"
            "Example:\n"
            "  export APP_USERNAME=admin\n"
            "  export APP_PASSWORD=yourpassword"
        )
        sys.exit(1)

    return username, password


def main() -> None:
    username, password = _load_credentials()

    auth = AuthService(username=username, password=password)
    store = DataStore()
    repository = FileRepository()

    store.load_items(repository.load())

    try:
        while not auth.is_locked:
            try:
                entered_username = _read_input("User: ")
                entered_password = _read_input("Pass: ")
            except EOFError as e:
                print(f"\n{e} Exiting.")
                return

            if auth.authenticate(entered_username, entered_password):
                break
        else:
            return  # Locked out after max attempts

    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
        return

    print("Welcome")

    try:
        while True:
            try:
                command = _read_input("What to do? (add/show/save/exit): ").strip().lower()
            except EOFError as e:
                print(f"\n{e} Exiting.")
                break

            if command == "exit":
                break
            elif command == "add":
                try:
                    value = _read_input("Value: ")
                except EOFError as e:
                    print(f"\n{e} Exiting.")
                    break
                try:
                    store.add_item(value)
                except ValueError as e:
                    print(f"Invalid input: {e}")
            elif command == "show":
                store.display_items()
            elif command == "save":
                repository.save(store.items)
            else:
                print(f"Unknown command: '{command}'. Use add, show, save, or exit.")

    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")


if __name__ == "__main__":
    main()
