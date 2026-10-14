# 📁 File Organizer & Duplicate File Finder

A Python-based mini-project that organizes files by category, identifies duplicate files using **SHA-256 hashing**, and displays file statistics and application activity history.

The application is designed to make file management easier, safer, and more organized through a simple menu-driven interface.

## ✨ Features

- **📂 File Organization:** Automatically categorizes files into Documents, Images, Videos, Audio, Archives, and Others.
- **🔍 Duplicate Detection:** Identifies duplicate files by comparing their SHA-256 hashes.
- **📊 File Statistics:** Displays total file count, storage usage, and category-wise statistics.
- **📝 Activity History:** Records application activities with timestamps.
- **🛡️ Safe File Handling:** Avoids overwriting existing files and does not automatically delete duplicate files.
- **🧪 Automated Testing:** Includes 28 unit tests using Python's built-in `unittest` framework.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| `pathlib` | File and folder path handling |
| `hashlib` | SHA-256 hashing for duplicate detection |
| `json` | Activity history storage |
| `unittest` | Automated testing |

## 📂 Project Structure

```text
file-organizer-duplicate-finder/
├── main.py
├── file_organizer.py
├── duplicate_finder.py
├── utils.py
├── activity_logger.py
├── activity_log.json
├── FileOrganizerDemo/
│   ├── Audio/
│   ├── Documents/
│   └── Images/
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

> Note: `activity_log.json` is generated locally and excluded from Git tracking, so it may not appear in the GitHub repository.

## ⚙️ Requirements

- Python 3.10 or later recommended
- No external Python packages required for the current features
- Windows, macOS, or Linux with Python installed

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/gungunsharma002300/file-organizer-duplicate-finder.git
```

### 2. Open the Project Directory

```bash
cd file-organizer-duplicate-finder
```

### 3. Run the Application

```bash
python main.py
```

If your system uses the `python3` command, run `python3 main.py` instead.

### 4. Use the Application

Choose an option from the menu and enter the folder path when prompted.

## 🖥️ Application Menu

```text
FILE ORGANIZER & DUPLICATE FILE FINDER

1. Organize Files
2. Find Duplicate Files
3. View File Statistics
4. View Activity / Results
5. Exit
```

## 🧪 Run Automated Tests

From the project root, execute:

```bash
python -m unittest discover -s tests -v
```

**Latest verified test result:** 28 tests passed successfully.

The tests cover file categorization, file organization, duplicate detection, file hashing, statistics, activity logging, and invalid or missing paths.

## 📸 Screenshots

The `screenshots/` folder contains application screenshots demonstrating the menu, file organization, duplicate reports, statistics, activity history, and exit message.

Open the folder in this repository to view the available screenshots.

## 🔐 Safety Notes

- Test file organization on a sample folder before using it on important files, because the organizer moves files.
- Duplicate detection reports matching files without automatically deleting them.
- SHA-256 hashes are used to compare file contents.
- Existing destination files are protected against accidental overwriting.
- Activity history is stored locally in `activity_log.json` and excluded from Git tracking.

## 👥 Team

Developed as a two-member BCA mini-project.

## 🔮 Future Enhancements

- Graphical user interface (GUI)
- Exportable file statistics and duplicate reports
- Additional file organization options
- Improved reporting and usability

---

*Developed using Python for practical file management and duplicate detection.*