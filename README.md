# ZipTool

# A CLI tool for versioned ZIP backups of files and directories.

---

## Features

- Recursive directory zipping
- File and folder exclusion
- Versioned + Timestamped backups 
- Configurable compression level
- Configurable
- Strict exclude mode

---

## Installation

# Install from Github
```bash
pip install git+https://github.com/chigmer/ZipTool.git
```

## Example Usage:
--show help message
```bash
ziptool -h
```
--zip current working directory, excluding .git and using a compress level of 9
```bash
ziptool . -v -X .git -cl 9
```
