
from pathlib import Path

from file_organizer import organize_files
from duplicate_finder import find_duplicates
from utils import get_file_statistics, format_size
from activity_logger import log_activity, display_activity_history


def get_folder_path():
    """Ask for a folder path and validate it."""
    folder_input = input(
        "\nEnter the folder path to scan: "
    ).strip().strip('"')

    folder = Path(folder_input)

    if not folder.exists():
        print("Error: This folder does not exist.")
        return None

    if not folder.is_dir():
        print("Error: The given path is not a folder.")
        return None

    return folder


def organize_menu():
    """Organize files and record the activity."""
    folder = get_folder_path()

    if folder is None:
        return

    try:
        summary = organize_files(folder)

        print("\n========== ORGANIZATION REPORT ==========")

        for category, count in summary.items():
            print(f"{category}: {count}")

        log_activity(
            "Organize Files",
            f"Folder: {folder} | Result: {summary}",
        )

        print("\nFile organization completed.")

    except (OSError, ValueError) as error:
        print(f"Could not organize files: {error}")


def duplicate_menu():
    """Find duplicates and record the result."""
    folder = get_folder_path()

    if folder is None:
        return

    try:
        result = find_duplicates(folder)

        print("\n========== DUPLICATE FILE REPORT ==========")
        print("Files scanned:", result["total_files_scanned"])
        print("Duplicate groups:", result["total_duplicate_groups"])
        print(
            "Files in duplicate groups:",
            result["total_duplicate_files"],
        )

        for number, group in enumerate(
            result["duplicate_groups"], start=1
        ):
            print(f"\nDuplicate Group {number}:")

            for file_path in group:
                print(f"  - {file_path}")

        if not result["duplicate_groups"]:
            print("\nNo duplicate files found.")

        if result["errors"]:
            print("\nSome files could not be read:")

            for error in result["errors"]:
                print(f"  - {error['file']}: {error['error']}")

        log_activity(
            "Find Duplicates",
            f"Folder: {folder} | Files scanned: "
            f"{result['total_files_scanned']} | "
            f"Duplicate groups: "
            f"{result['total_duplicate_groups']}",
        )

        print("\nNo files were deleted.")

    except (OSError, ValueError) as error:
        print(f"Could not scan folder: {error}")


def statistics_menu():
    """Show file statistics and record the operation."""
    folder = get_folder_path()

    if folder is None:
        return

    try:
        result = get_file_statistics(folder)

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

        duplicate_result = find_duplicates(folder)

        print("\n========== DUPLICATE SUMMARY ==========")
        print(
            "Duplicate groups:",
            duplicate_result["total_duplicate_groups"],
        )
        print(
            "Files in duplicate groups:",
            duplicate_result["total_duplicate_files"],
        )

        log_activity(
            "File Statistics",
            f"Folder: {folder} | Total files: "
            f"{result['total_files']} | Storage: "
            f"{format_size(result['total_size_bytes'])}",
        )

    except (OSError, ValueError) as error:
        print(f"Could not calculate statistics: {error}")


def main():
    """Display the application menu."""
    while True:
        print("\n" + "=" * 45)
        print(" FILE ORGANIZER & DUPLICATE FILE FINDER")
        print("=" * 45)
        print("1. Organize Files")
        print("2. Find Duplicate Files")
        print("3. View File Statistics")
        print("4. View Activity / Results")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            organize_menu()

        elif choice == "2":
            duplicate_menu()

        elif choice == "3":
            statistics_menu()

        elif choice == "4":
            display_activity_history()

        elif choice == "5":
            print("\nThank you for using the application!")
            break

        else:
            print("\nInvalid choice. Please enter 1 to 5.")


if __name__ == "__main__":
    main()
