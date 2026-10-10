
from pathlib import Path

from file_organizer import get_file_category


def get_file_statistics(folder_path):
    """Calculate file counts and storage size by category."""
    folder = Path(folder_path)

    # Check whether the folder exists.
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    # Check whether the given path is a directory.
    if not folder.is_dir():
        raise NotADirectoryError(f"Not a folder: {folder}")

    # Define the file categories.
    categories = [
        "Documents",
        "Images",
        "Videos",
        "Audio",
        "Archives",
        "Others",
    ]

    # Initialize statistics for each category.
    statistics = {
        category: {
            "count": 0,
            "size_bytes": 0,
        }
        for category in categories
    }

    total_files = 0
    total_size_bytes = 0
    errors = []

    # Scan files directly inside the selected folder.
    for file_path in folder.iterdir():

        # Skip folders and process only files.
        if not file_path.is_file():
            continue

        try:
            # Get the file size and category.
            file_size = file_path.stat().st_size
            category = get_file_category(file_path)

            # Update category-wise statistics.
            statistics[category]["count"] += 1
            statistics[category]["size_bytes"] += file_size

            # Update overall statistics.
            total_files += 1
            total_size_bytes += file_size

        except OSError as error:
            # Record files that could not be accessed.
            errors.append({
                "file": str(file_path),
                "error": str(error),
            })

    # Return all calculated statistics.
    return {
        "total_files": total_files,
        "total_size_bytes": total_size_bytes,
        "categories": statistics,
        "errors": errors,
    }


def format_size(size_bytes):
    """Convert bytes into a readable storage size."""
    size = float(size_bytes)
    units = ["B", "KB", "MB", "GB", "TB"]

    for unit in units:
        if size < 1024 or unit == "TB":
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} TB"


if __name__ == "__main__":
    folder_input = input(
        "Enter folder path for statistics: "
    ).strip().strip('"')

    try:
        result = get_file_statistics(folder_input)

        print("\n========== FILE STATISTICS ==========")
        print("Total files:", result["total_files"])
        print(
            "Total storage:",
            format_size(result["total_size_bytes"]),
        )

        print("\nCategory-wise details:")

        for category, details in result["categories"].items():
            print(
                f"{category}: {details['count']} files, "
                f"{format_size(details['size_bytes'])}"
            )

        if result["errors"]:
            print("\nSome files could not be read:")

            for error in result["errors"]:
                print(f"  - {error['file']}: {error['error']}")

    except (OSError, ValueError) as error:
        print(f"Error: {error}")
