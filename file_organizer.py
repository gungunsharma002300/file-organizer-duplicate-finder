
from pathlib import Path
import shutil


# File extensions grouped by category
FILE_CATEGORIES = {
    "Documents": [
        ".pdf", ".doc", ".docx", ".txt",
        ".ppt", ".pptx", ".xls", ".xlsx", ".csv"
    ],
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"
    ],
    "Videos": [
        ".mp4", ".mkv", ".mov", ".avi"
    ],
    "Audio": [
        ".mp3", ".wav", ".aac", ".flac"
    ],
    "Archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz"
    ],
}


def get_file_category(file_path):
    """Return a file category based on its extension."""
    extension = Path(file_path).suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


def scan_files(folder_path):
    """Return files directly inside the selected folder."""
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    if not folder.is_dir():
        raise NotADirectoryError(f"Not a folder: {folder}")

    return [
        item for item in folder.iterdir()
        if item.is_file()
    ]


def get_unique_destination(destination):
    """Return a destination that does not already exist."""
    destination = Path(destination)

    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_destination = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )

        if not new_destination.exists():
            return new_destination

        counter += 1


def organize_files(folder_path):
    """Organize files into category folders safely."""
    folder = Path(folder_path)

    # Validate the folder before organizing.
    files = scan_files(folder)

    summary = {
        category: 0 for category in FILE_CATEGORIES
    }
    summary["Others"] = 0
    summary["Errors"] = 0

    for file_path in files:
        try:
            category = get_file_category(file_path)
            category_folder = folder / category

            category_folder.mkdir(exist_ok=True)

            destination = get_unique_destination(
                category_folder / file_path.name
            )

            shutil.move(str(file_path), str(destination))
            summary[category] += 1

        except (OSError, shutil.Error) as error:
            print(
                f"Could not move {file_path.name}: {error}"
            )
            summary["Errors"] += 1

    return summary
