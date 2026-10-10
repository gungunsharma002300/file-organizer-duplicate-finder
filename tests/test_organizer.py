
import tempfile
import unittest
from pathlib import Path

from file_organizer import (
    get_file_category,
    scan_files,
    get_unique_destination,
    organize_files,
)


class TestFileCategory(unittest.TestCase):

    def test_document_file(self):
        self.assertEqual(
            get_file_category("notes.pdf"), "Documents"
        )

    def test_image_uppercase_extension(self):
        self.assertEqual(
            get_file_category("photo.JPG"), "Images"
        )

    def test_audio_file(self):
        self.assertEqual(
            get_file_category("song.mp3"), "Audio"
        )

    def test_unknown_extension(self):
        self.assertEqual(
            get_file_category("data.xyz"), "Others"
        )


class TestScanFiles(unittest.TestCase):

    def test_scan_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            (folder / "notes.txt").write_text(
                "Hello", encoding="utf-8"
            )
            (folder / "photo.jpg").write_text(
                "Image", encoding="utf-8"
            )
            (folder / "subfolder").mkdir()

            files = scan_files(folder)

            self.assertEqual(len(files), 2)
            self.assertTrue(
                all(file.is_file() for file in files)
            )

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


class TestFileOrganization(unittest.TestCase):

    def test_organize_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            (folder / "notes.txt").write_text(
                "Document", encoding="utf-8"
            )
            (folder / "photo.jpg").write_text(
                "Image", encoding="utf-8"
            )
            (folder / "unknown.xyz").write_text(
                "Other", encoding="utf-8"
            )

            summary = organize_files(folder)

            self.assertTrue(
                (folder / "Documents" / "notes.txt").exists()
            )
            self.assertTrue(
                (folder / "Images" / "photo.jpg").exists()
            )
            self.assertTrue(
                (folder / "Others" / "unknown.xyz").exists()
            )

            self.assertEqual(summary["Documents"], 1)
            self.assertEqual(summary["Images"], 1)
            self.assertEqual(summary["Others"], 1)
            self.assertEqual(summary["Errors"], 0)

    def test_existing_filename_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            images = folder / "Images"
            images.mkdir()

            (folder / "photo.jpg").write_text(
                "New image", encoding="utf-8"
            )
            (images / "photo.jpg").write_text(
                "Existing image", encoding="utf-8"
            )

            summary = organize_files(folder)

            self.assertEqual(summary["Images"], 1)
            self.assertEqual(
                (images / "photo.jpg").read_text(encoding="utf-8"),
                "Existing image",
            )
            self.assertEqual(
                (images / "photo_1.jpg").read_text(encoding="utf-8"),
                "New image",
            )

    def test_unique_destination(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            original = folder / "report.txt"
            original.write_text("Existing", encoding="utf-8")

            destination = get_unique_destination(original)

            self.assertEqual(destination.name, "report_1.txt")


if __name__ == "__main__":
    unittest.main()
