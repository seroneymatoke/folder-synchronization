I apologize for the oversight. Let's fix that. Here's a more detailed `README.md` written completely in Markdown for your file synchronization tool:

---

# File Synchronization Tool 📂

A robust tool designed to mirror the content of one directory (source) into another (replica). It offers efficient synchronization with data integrity checks and real-time progress feedback.

## 🌟 Features:

- **Data Integrity**: Post-synchronization MD5 integrity checks for all files.
- **Parallel Processing**: Uses multithreading to handle multiple files concurrently.
- **Progress Tracking**: Real-time progress bar to monitor synchronization.
- **Detailed Logging**: Detailed event logs, including actions on individual files.

## 🚀 Quick Start

### 1. Installation:

Clone the repository and navigate to its root directory:

```bash
git clone [https://github.com/seroneymatoke]
cd [folder-synchronization]
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Usage:

Run the synchronization tool using:

```bash
python src/main.py --source [SOURCE_PATH] --replica [REPLICA_PATH]
```

##### Command-Line Arguments:

- `--source`: Path to the source directory.
- `--replica`: Path to the replica directory.
- `--interval`: No of seconds to the next sync.
- `--log_file`: (Optional) Path to save logs. Default is `./sync.log`.
- `--log_level`: (Optional) Logging level (`INFO`, `DEBUG`, etc.). Default is `INFO`.
- `--max_workers`: (Optional) Number of threads for parallel processing. Default is system's max possible.

## 🔧 Running Tests:

Ensure you have `pytest` installed:

```bash
pip install pytest
```

Then, from the project's root directory:

```bash
pytest tests/
```

## 📝 Contributing:

Contributions, issues, and feature requests are welcome! Before making any major changes, please open an issue first to discuss what you'd like to change. Make sure to update tests as appropriate.

## 📜 License:

[MIT](https://choosealicense.com/licenses/mit/)

---