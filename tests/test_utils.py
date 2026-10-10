
import tempfile
import unittest
from pathlib import Path

from utils import get_file_statistics, format_size


class TestFileStatistics(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_counts_files_and_storage(self):
        (self.folder / "notes.txt").write_text(
            "Hello", encoding="utf-8"
        )
        (self.folder / "photo.jpg").write_bytes(
            b"image-data"
        )

        result = get_file_statistics(self.folder)

        self.assertEqual(result["total_files"], 2)
        self.assertEqual(
            result["total_size_bytes"],
            5 + len(b"image-data")
        )
        self.assertEqual(
            result["categories"]["Documents"]["count"], 1
        )
        self.assertEqual(
            result["categories"]["Images"]["count"], 1
        )

    def test_empty_folder(self):
        result = get_file_statistics(self.folder)

        self.assertEqual(result["total_files"], 0)
        self.assertEqual(result["total_size_bytes"], 0)

    def test_ignores_subfolders(self):
        (self.folder / "notes.txt").write_text(
            "Hello", encoding="utf-8"
        )
        (self.folder / "subfolder").mkdir()

        result = get_file_statistics(self.folder)

        self.assertEqual(result["total_files"], 1)

    def test_missing_folder(self):
        missing = self.folder / "does_not_exist"

        with self.assertRaises(FileNotFoundError):
            get_file_statistics(missing)

    def test_path_is_a_file(self):
        file_path = self.folder / "notes.txt"
        file_path.write_text("Hello", encoding="utf-8")

        with self.assertRaises(NotADirectoryError):
            get_file_statistics(file_path)

    def test_format_size(self):
        self.assertEqual(format_size(0), "0.00 B")
        self.assertEqual(format_size(1024), "1.00 KB")
        self.assertEqual(format_size(1048576), "1.00 MB")


if __name__ == "__main__":
    unittest.main()
