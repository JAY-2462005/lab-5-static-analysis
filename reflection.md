# Lab 5: Static Code Analysis

This repository contains the work for Lab 5, demonstrating the use of Pylint, Bandit, and Flake8 to analyze and improve Python code.

## Files

* `inventory_system_original.py`: The original, unfixed Python script.
* `inventory_system_cleaned.py`: The final, cleaned version of the script with all issues resolved.
* `pylint_report.txt`: The initial report from Pylint on the original file.
* `bandit_report.txt`: The initial report from Bandit on the original file.
* `flake8_report.txt`: The initial report from Flake8 on the original file.
* `pylint_fixed_report.txt`: The final report from Pylint on the cleaned file (verifying fixes).
* `bandit_fixed_report.txt`: The final report from Bandit on the cleaned file (verifying fixes).
* `flake8_fixed_report.txt`: The final report from Flake8 on the cleaned file (verifying fixes).

---

## Issue & Fix Table

[cite_start]This table documents the primary issues found in the *original* code [cite: 1, 4, 100] and the fixes applied to create `inventory_system_cleaned.py`.

| Issue | Tool(s) | Type / ID | Line(s) (Orig) | Description | Fix Approach (in Final Code) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Use of `eval()`** | Bandit / Pylint | Medium (Bandit B307) / Warning (Pylint W0123) | 59 | [cite_start]`eval()` was used[cite: 1, 6], which is a critical security vulnerability. | Removed the `eval()` call entirely and replaced it with a simple `print()` statement. |
| **Mutable Default Argument** | Pylint | Warning (W0102) | 8 | [cite_start]The `logs=[]` argument is mutable[cite: 1], causing it to be shared across all function calls. | Changed the default argument to `logs=None` and initialized `logs = []` inside the function body. |
| **Bare `except` / `pass`** | Pylint / Bandit / Flake8 | Warning (Pylint W0702) / Low (Bandit B110) / Error (Flake8 E722) | 19-20 | [cite_start]A bare `except: pass` statement was used[cite: 1, 5, 100], which hides all errors and bugs. | Replaced the bare `except:` with specific `except KeyError:` and `except TypeError as e:`, both with proper logging. |
| **Missing `with` for Files** | Pylint | Warning (R1732, W1514) | 26, 32 | [cite_start]Files were opened without a `with` statement or specified encoding[cite: 1, 2]. | Refactored `load_data` and `save_data` to use the `with open(..., encoding="utf-8") as f:` context manager. |
| **Unused Import** | Flake8 / Pylint | Error (Flake8 F401) / Warning (Pylint W0611) | 2 | [cite_start]`import logging` was included but never used[cite: 1, 100]. | Implemented `logging.basicConfig()` in `main()` and added `logging.info/warning/error` calls throughout the script. |
| **Invalid Naming** | Pylint | Convention (C0103) | 8, 14, etc. | [cite_start]Function names like `addItem` and `loadData` did not conform to `snake_case`[cite: 1, 2, 3]. | Renamed all functions to `snake_case` (e.g., `add_item`, `load_data`) for PEP 8 compliance. |
| **Missing Docstrings** | Pylint | Convention (C0114, C0116) | 1, 8, 14, etc. | [cite_start]The module and all functions were missing docstrings[cite: 1]. | Added a module-level docstring and detailed docstrings (including Args/Returns) for all functions. |
| **Missing Final Newline** | Pylint / Flake8 | Convention (C0304) / Warning (W292) | 61 | [cite_start]The file did not end with a final newline character[cite: 1, 100]. | Added a final blank line at the end of the file. |

---

## Reflections

### 1. Easiest vs. Hardest Fixes

* [cite_start]**Easiest:** The easiest fixes were the mechanical ones reported by Flake8 and Pylint, such as renaming functions to `snake_case` (like `addItem` to `add_item`) [cite: 1][cite_start], adding the missing final newline [cite: 1, 100][cite_start], and removing the obviously dangerous `eval()` function[cite: 1, 6]. These required little thought, just direct action.
* [cite_start]**Hardest:** The hardest fix conceptually was the **`mutable default argument`** (`logs=[]`)[cite: 1]. This is a subtle logical bug that doesn't cause a crash but leads to incorrect behavior. Understanding *why* the list is shared and the correct `if logs is None:` pattern took more thought than a simple syntax fix.

### 2. False Positives

I did not encounter any significant false positives in this lab. All the issues reported by the tools, especially the high and medium-severity ones, pointed to real problems:
* [cite_start]Bandit's `eval()` warning [cite: 6] was critical.
* [cite_start]Pylint's `dangerous-default-value` [cite: 1] warning was a real, subtle bug.
* [cite_start]All three tools correctly identified the `bare-except` [cite: 1, 5, 100] as a major problem.

### 3. Integrating Static Analysis

I would integrate these tools into my workflow in two key places:

1.  **Local Development (IDE):** I would install the Pylint and Flake8 extensions in my editor (like VS Code). This provides real-time feedback (squiggles) as I type, allowing me to fix style and simple bugs instantly.
2.  **Continuous Integration (CI) Pipeline:** I would add a step in my GitHub Actions (or similar) workflow to run `pylint`, `flake8`, and `bandit` on every pull request. [cite_start]This acts as an automated "gatekeeper"[cite: 98], preventing code with high-severity issues or major style violations from being merged into the main branch.

### 4. Observed Improvements

The code quality is tangibly better after applying the fixes:

* **Robustness:** The code is far more robust. The `remove_item` and `get_qty` functions no longer crash if you use a non-existent item. The `add_item` function's logging now works correctly without sharing state.
* [cite_start]**Security:** The most critical improvement was removing the `eval()` call[cite: 1, 6], which eliminated a major security vulnerability.
* **Maintainability & Readability:** The code is now much easier to read. Using `with open()` for files, adding `docstrings` for all functions, and enforcing `snake_case` naming makes the code professional and simple for a new developer to understand.