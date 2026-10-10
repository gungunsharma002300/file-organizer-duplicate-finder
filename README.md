# File Organizer & Duplicate File Finder

A Python-based mini-project that organizes files, detects duplicate files using SHA-256 hashing, and displays file statistics and activity history.

## Features

- **File Organization:** Categorizes files into Documents, Images, Videos, Audio, Archives, and Others.
- **Duplicate Detection:** Identifies duplicate files by comparing SHA-256 hashes.
- **File Statistics:** Displays file counts, category-wise storage usage, and total storage.
- **Activity History:** Records application activities with timestamps.
- **Safe Handling:** Avoids overwriting existing files and does not automatically delete duplicates.
- **Automated Tests:** Uses Python's built-in `unittest` framework.

## Technologies Used

- Python 3
- pathlib
- hashlib
- json
- unittest

## Project Structure

```text
file-organizer-duplicate-finder/
├── main.py
├── file_organizer.py
├── duplicate_finder.py
├── utils.py
├── activity_logger.py
├── tests/
│   ├── test_activity_logger.py
│   ├── test_duplicate_finder.py
│   ├── test_organizer.py
│   └── test_utils.py
├── sample_data/
├── screenshots/
├── docs/
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or later recommended
- No external Python packages required for the current features

## How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/gungunsharma002300/file-organizer-duplicate-finder.git
   ```

2. Open the project directory:

   ```bash
   cd file-organizer-duplicate-finder
   ```

3. Run the application:

   ```bash
   python main.py
   ```

4. Choose an option from the menu and enter the folder path when prompted.

## Application Menu

1. Organize Files
2. Find Duplicate Files
3. View File Statistics
4. View Activity / Results
5. Exit

## Run Automated Tests

From the project root, run:

```bash
python -m unittest discover -s tests -v
```

The project currently has 28 passing automated tests.

## Safety Notes

- Test file organization on a sample folder first because the organizer moves files.
- The duplicate finder reports duplicate groups without deleting files.
- The local activity history is stored in `activity_log.json`, which is excluded from Git tracking.

## Team

Developed as a two-member BCA mini-project.

## Future Enhancements

- Graphical user interface
- Exportable reports
- Additional file organization options
