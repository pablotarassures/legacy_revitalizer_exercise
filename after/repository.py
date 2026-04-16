from typing import List

from models import Item


class FileRepository:
    """Handles persistence — reading and writing items to disk."""

    def __init__(self, filepath: str = "data.txt"):
        self._filepath = filepath

    def save(self, items: List[Item]) -> None:
        if not items:
            print("Nothing to save.")
            return
        try:
            with open(self._filepath, "w") as f:
                for item in items:
                    f.write(f"{item.id},{item.value},{item.created_at}\n")
            print("Saved.")
        except PermissionError:
            print(f"Error: no write permission for '{self._filepath}'.")
        except OSError as e:
            print(f"Error saving data: {e}")

    def load(self) -> List[Item]:
        """Load items from disk. Returns an empty list if the file does not exist."""
        try:
            with open(self._filepath, "r") as f:
                items = []
                for line_number, line in enumerate(f, start=1):
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(",", 2)
                    if len(parts) != 3:
                        print(f"Warning: skipping malformed line {line_number}.")
                        continue
                    try:
                        item = Item(id=int(parts[0]), value=parts[1], created_at=parts[2])
                        items.append(item)
                    except ValueError:
                        print(f"Warning: skipping invalid data on line {line_number}.")
                return items
        except FileNotFoundError:
            return []  # No saved data yet — not an error
        except PermissionError:
            print(f"Error: no read permission for '{self._filepath}'.")
            return []
        except OSError as e:
            print(f"Error loading data: {e}")
            return []
