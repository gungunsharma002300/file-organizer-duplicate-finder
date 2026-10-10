
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import activity_logger


class TestActivityLogger(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_path = Path(self.temp_dir.name) / "test_log.json"
        self.log_file_patch = patch.object(
            activity_logger, "LOG_FILE", self.log_path
        )
        self.log_file_patch.start()

    def tearDown(self):
        self.log_file_patch.stop()
        self.temp_dir.cleanup()

    def test_log_activity_saves_record(self):
        result = activity_logger.log_activity(
            "Test Action", "Test details"
        )

        self.assertTrue(result)
        history = json.loads(
            self.log_path.read_text(encoding="utf-8")
        )
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["action"], "Test Action")
        self.assertEqual(history[0]["details"], "Test details")
        self.assertIn("timestamp", history[0])

    def test_history_is_newest_first(self):
        activity_logger.log_activity("First", "First record")
        activity_logger.log_activity("Second", "Second record")

        history = activity_logger.get_activity_history()

        self.assertEqual(history[0]["action"], "Second")
        self.assertEqual(history[1]["action"], "First")

    def test_missing_log_returns_empty_list(self):
        self.assertEqual(
            activity_logger.get_activity_history(), []
        )

    def test_invalid_json_returns_empty_list(self):
        self.log_path.write_text("{invalid json", encoding="utf-8")

        self.assertEqual(
            activity_logger.get_activity_history(), []
        )


if __name__ == "__main__":
    unittest.main()
