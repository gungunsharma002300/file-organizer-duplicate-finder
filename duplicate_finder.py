
from pathlib import Path
import hashlib


def calculate_file_hash(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(4096)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


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


def find_duplicates(folder_path):
    """Find files having identical content."""
    files = scan_files(folder_path)
    hash_groups = {}
    errors = []

    for file_path in files:
        try:
            file_hash = calculate_file_hash(file_path)

            if file_hash not in hash_groups:
                hash_groups[file_hash] = []

            hash_groups[file_hash].append(file_path)

        except OSError as error:
            errors.append({
                "file": str(file_path),
                "error": str(error),
            })

    duplicates = [
        paths
        for paths in hash_groups.values()
        if len(paths) > 1
    ]

    return {
        "duplicate_groups": duplicates,
        "total_files_scanned": len(files),
        "total_duplicate_groups": len(duplicates),
        "total_duplicate_files": sum(
            len(group) for group in duplicates
        ),
        "errors": errors,
    }


if __name__ == "__main__":
    folder = input("Enter folder path to scan: ").strip().strip('"')

    try:
        result = find_duplicates(folder)

        print("\n========== DUPLICATE FILE REPORT ==========")
        print(
            "Files scanned:",
            result["total_files_scanned"]
        )
        print(
            "Duplicate groups:",
            result["total_duplicate_groups"]
        )
        print(
            "Files belonging to duplicate groups:",
            result["total_duplicate_files"]
        )

        if result["duplicate_groups"]:
            for number, group in enumerate(
                result["duplicate_groups"], start=1
            ):
                print(f"\nDuplicate Group {number}:")

                for file_path in group:
                    print(f"  - {file_path}")
        else:
            print("\nNo duplicate files found.")

        if result["errors"]:
            print("\nSome files could not be read:")
            for error in result["errors"]:
                print(f"  - {error['file']}: {error['error']}")

    except (OSError, ValueError) as error:
        print(f"Error: {error}")
