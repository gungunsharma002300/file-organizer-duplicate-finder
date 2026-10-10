
import json
from datetime import datetime
from pathlib import Path


# Store activity history in the main project folder.
LOG_FILE = Path(__file__).parent / "activity_log.json"


def log_activity(action, details):
    """Save an activity with its date and time."""
    entry = {
        "timestamp": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "action": action,
        "details": details,
    }

    try:
        if LOG_FILE.exists():
            with LOG_FILE.open("r", encoding="utf-8") as file:
                history = json.load(file)

            if not isinstance(history, list):
                history = []
        else:
            history = []

    except (OSError, json.JSONDecodeError):
        history = []

    history.append(entry)

    try:
        with LOG_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                history,
                file,
                indent=4,
                ensure_ascii=False,
            )
        return True

    except OSError as error:
        print(f"Warning: Could not save activity: {error}")
        return False


def get_activity_history():
    """Return saved activity records, newest first."""
    if not LOG_FILE.exists():
        return []

    try:
        with LOG_FILE.open("r", encoding="utf-8") as file:
            history = json.load(file)

        if not isinstance(history, list):
            return []

        return list(reversed(history))

    except (OSError, json.JSONDecodeError):
        print("Warning: Activity history could not be read.")
        return []


def display_activity_history():
    """Display the saved activity records."""
    history = get_activity_history()

    print("\n========== ACTIVITY HISTORY ==========")

    if not history:
        print("No activity recorded yet.")
        return

    for number, entry in enumerate(history, start=1):
        timestamp = entry.get("timestamp", "Unknown time")
        action = entry.get("action", "Unknown action")
        details = entry.get("details", "No details")

        print(f"\n{number}. {action}")
        print(f"   Date and time: {timestamp}")
        print(f"   Details: {details}")


if __name__ == "__main__":
    print("Activity Logger Test")
    log_activity(
        "Test",
        "Activity logger was tested successfully.",
    )
    display_activity_history()
