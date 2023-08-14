# File Synchronization Tool 📂

A robust tool designed to mirror the content of one directory (source) into another (replica). It offers efficient synchronization with data integrity checks and real-time progress feedback.

## 🌟 Features:

- **Data Integrity**: Post-synchronization MD5 integrity checks for all files.
- **Parallel Processing**: Uses multithreading to handle multiple files concurrently.
- **Progress Tracking**: Real-time progress bar to monitor synchronization.
- **Detailed Logging**: Detailed event logs, including actions on individual files.

## 🚀 Quick Start
__
### 1. Installation:

#### Prerequisites

- Python 3.6 or newer: Ensure you have a compatible Python version installed. If not, download and install it from [Python's official website](https://python.org).
- pip: Python's package manager, which usually comes bundled with Python installations. More about pip can be found at the [pip documentation](https://pip.pypa.io/en/stable/).

Clone the repository and navigate to its root directory:

```bash
git clone https://github.com/seroneymatoke/folder-synchronization
cd folder-synchronization
```


#### Set Up a Virtual Environment(optional, but recommended):

It's a good practice to create a virtual environment for Python projects to manage dependencies cleanly. Here's how you can do it:

- Install `virtualenv` if you haven't already:
  ```
  pip install virtualenv
  ```
  More about `virtualenv` can be found at the [official documentation](https://virtualenv.pypa.io/en/latest/).

- Create a virtual environment:
  ```
  virtualenv venv
  ```

- Activate the virtual environment:

  - On Windows:
    ```
    .\venv\Scripts\activate
    ```

  - On macOS and Linux:
    ```
    source venv/bin/activate
    ```

#### Install Required Libraries:

Install the necessary libraries using `pip`:


Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Usage:
__
Run the synchronization tool using:

```bash
python src/main.py --source [SOURCE_PATH] --replica [REPLICA_PATH]
```

##### Command-Line Arguments:

- `--source`: Path to the source directory.
- `--replica`: Path to the replica directory.
- `--interval`: No of seconds to the next sync.
- `--log_file`: (Optional) Path to save logs. Default is `sync.log`.
- `--log_level`: (Optional) Logging level (`INFO`, `DEBUG`, etc.). Default is `INFO`.
- `--max_workers`: (Optional) Number of threads for parallel processing. Default is system's max possible.

### 3. 🔧 Running Tests:
__
Ensure you have `pytest` installed:

```bash
pip install pytest
```

Then, from the project's root directory:

```bash
pytest tests/
```

### 4.  📝 Contributing:
__
Contributions, issues, and feature requests are welcome! Before making any major changes, please open an issue first to discuss what you'd like to change. Make sure to update tests as appropriate.

### 5. 📜 License:

[MIT](https://choosealicense.com/licenses/mit/)

---