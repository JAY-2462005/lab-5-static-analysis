
# Lab 5: Static Code Analysis

This repository contains the work for Lab 5, demonstrating the use of Pylint, Bandit, and Flake8 to analyze and improve Python code.

## Files
* `inventory_system_original.py`: The original, unfixed Python script.
* `inventory_system_cleaned.py`: The final, cleaned version of the script.
* `pylint_report.txt`: Initial report from Pylint.
* `bandit_report.txt`: Initial report from Bandit.
* `flake8_report.txt`: Initial report from Flake8.
* `..._fixed_report.txt`: Final reports after applying fixes.

---

## Issue & Fix Table

Here is a summary of the issues identified and fixed.

| Issue | Tool | Type / Severity | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Mutable Default Argument** | Pylint | Warning | 11 | The `logs=[]` argument is mutable and shared across all calls to `addItem`. | Changed default to `None` and initialized `logs = []` inside the function if `logs is None`. |
| **Use of `eval`** | Bandit | High Severity | 70 | `eval()` is used, which is a major security risk as it can execute arbitrary code. | Removed the `eval()` call and replaced it with a simple `print()` statement. |
| **Bare `except:`** | Pylint | Warning | 20 | Using `except:` catches all exceptions, including `SystemExit`, which can hide bugs. | Replaced `except:` with `except KeyError:` to specifically catch the error of a missing item. |
| **Missing file `close()` / No `with`** | Pylint | Warning | 26, 31 | Files are opened but not properly closed in `loadData` and `saveData`, which can lead to resource leaks. | Re-wrote both functions to use the `with open(...) as f:` context manager, which handles closing automatically. |
| **Old String Formatting** | Pylint | Convention | 14 | Uses old `%` string formatting. | Converted the string to an f-string for better readability. |
| **`getQty` Unsafe Access** | Bug | High | 23 | `getQty` directly accesses `stock_data[item]`, which will raise a `KeyError` if the item doesn't exist. | Changed `return stock_data[item]` to `return stock_data.get(item, 0)` to safely return 0 for missing items. |

---

## Reflections

### 1. Easiest vs. Hardest Fixes

* **Easiest:** The easiest fixes were warnings from Flake8 (like whitespace) and simple Pylint convention warnings, like changing the old string formatting (`%`) to an f-string. Removing the `eval()` call from Bandit was also easy, as it was clearly unnecessary.
* **Hardest:** The "mutable default argument" was the hardest conceptually. It's a subtle bug that isn't an immediate crash but causes strange behavior over time. Understanding *why* the list is shared and the correct `if logs is None:` pattern took more thought.

### 2. False Positives

* In this specific lab, there were no obvious false positives. All the high and medium-severity warnings were valid and pointed to real issues.
* *(Example of a potential false positive):* Pylint might flag a variable as `unused-variable` in a complex `try...except` block if it's only used in one of the `except` clauses. Or, Bandit might flag a `subprocess` command as a security risk, even if the command is hard-coded and doesn't take user input, making it safe.

### 3. Integrating Static Analysis

I would integrate these tools into my workflow in two key places:
1.  **Local Development:** I'd install them as part of my IDE (like the VS Code Python extension). This provides real-time feedback (squiggles) as I type, allowing me to fix style and simple bugs instantly.
2.  **Continuous Integration (CI):** I would add a step to my GitHub Actions (or other CI pipeline) that runs `flake8`, `pylint`, and `bandit` on every pull request. This would act as an automated gatekeeper, preventing code with high-severity issues or major style violations from being merged into the `main` branch.

### 4. Observed Improvements

After applying the fixes, the code is tangibly better:
* **Robustness:** The code is far more robust. The `removeItem` and `getQty` functions no longer crash if you try to use a non-existent item. The `addItem` function no longer has the subtle `logs` bug.
* **Security:** The most significant improvement was removing the `eval()` call, which eliminated a critical security vulnerability.
* **Readability:** Using `with open(...)` and f-strings makes the code more modern, maintainable, and easier to read.