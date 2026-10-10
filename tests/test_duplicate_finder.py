
import tempfile
import unittest
from pathlib import Path

from duplicate_finder import (
    calculate_file_hash,
    scan_files,
    find_duplicates,
)


class TestCalculateFileHash(unittest.TestCase):

    def test_same_content_has_same_hash(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            file1 = folder / "first.txt"
            file2 = folder / "second.txt"

            file1.write_text("Hello World", encoding="utf-8")
            file2.write_text("Hello World", encoding="utf-8")

            self.assertEqual(
                calculate_file_hash(file1),
                calculate_file_hash(file2),
            )

    def test_different_content_has_different_hash(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            file1 = folder / "first.txt"
            file2 = folder / "second.txt"

            file1.write_text("Hello", encoding="utf-8")
            file2.write_text("Goodbye", encoding="utf-8")

            self.assertNotEqual(
                calculate_file_hash(file1),
                calculate_file_hash(file2),
            )


class TestDuplicateScanning(unittest.TestCase):

    def test_scan_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            (folder / "first.txt").write_text(
                "Hello", encoding="utf-8"
            )
            (folder / "second.txt").write_text(
                "World", encoding="utf-8"
            )
            (folder / "subfolder").mkdir()

            files = scan_files(folder)

            self.assertEqual(len(files), 2)

    def test_missing_folder(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "missing"

            with self.assertRaises(FileNotFoundError):
                scan_files(missing)

    def test_path_is_a_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "notes.txt"
            file_path.write_text("Hello", encoding="utf-8")

            with self.assertRaises(NotADirectoryError):
                scan_files(file_path)


class TestFindDuplicates(unittest.TestCase):

    def test_finds_duplicate_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            (folder / "first.txt").write_text(
                "Same content", encoding="utf-8"
            )
            (folder / "copy.txt").write_text(
                "Same content", encoding="utf-8"
            )
            (folder / "different.txt").write_text(
                "Different content", encoding="utf-8"
            )

            result = find_duplicates(folder)

            self.assertEqual(result["total_files_scanned"], 3)
            self.assertEqual(result["total_duplicate_groups"], 1)
            self.assertEqual(result["total_duplicate_files"], 2)
            self.assertEqual(len(result["duplicate_groups"][0]), 2)
            self.assertEqual(result["errors"], [])

    def test_no_duplicates(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            (folder / "first.txt").write_text(
                "Alpha", encoding="utf-8"
            )
            (folder / "second.txt").write_text(
                "Beta", encoding="utf-8"
            )

            result = find_duplicates(folder)

            self.assertEqual(result["total_duplicate_groups"], 0)
            self.assertEqual(result["total_duplicate_files"], 0)

    def test_empty_folder(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = find_duplicates(temp_dir)

            self.assertEqual(result["total_files_scanned"], 0)
            self.assertEqual(result["total_duplicate_groups"], 0)
            self.assertEqual(result["total_duplicate_files"], 0)


if __name__ == "__main__":
    unittest.main()
