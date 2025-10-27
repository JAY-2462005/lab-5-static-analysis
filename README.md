# Lab 5: Static Code Analysis

This repository contains the work for Lab 5, demonstrating the use of Pylint, Bandit, and Flake8 to analyze and improve Python code.

## Files
* `inventory_system_original.py`: The original, unfixed Python script.
* `inventory_system_cleaned.py`: The final, cleaned version of the script.
* `pylint_report.txt`: Initial report from Pylint.
* `bandit_report.txt`: Initial report from Bandit.
* `flake8_report.txt`: Initial report from Flake8.
* `pylint_fixed_report.txt`: Final report from Pylint after applying fixes.
* `bandit_fixed_report.txt`: Final report from Bandit after applying fixes.
* `flake8_fixed_report.txt`: Final report from Flake8 after applying fixes.

---

## Issue & Fix Table

Here is a summary of the issues identified from the initial reports and their corresponding fix approaches.

| Issue | Tool | Type / Severity | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Mutable Default Argument** | Pylint | Warning (`W0102`) | 11 | The `logs=[]` argument is a mutable default value, which can lead to unexpected shared state across function calls. | Change default to `None` and initialize `logs = []` inside the function if `logs is None`. |
| **Use of `eval()`** | Bandit | High (`B307`) | 70 | The `eval()` function is used, which is a major security vulnerability as it can execute arbitrary code injected by an attacker. | Remove the `eval()` call entirely and replace with a safe alternative, such as a direct `print()` statement or specific logic. |
| **Bare `except:` Statement** | Pylint | Warning (`W0702`) | 20 | Using a bare `except:` catches all exceptions, including system-exiting ones, and can mask legitimate programming errors. | Specify the exact exception to catch, e.g., `except KeyError:` for dictionary access issues, or `except Exception as e:` for general error logging. |
| **Missing `with` statement for file operations** | Pylint | Error (`W0102` related) | 26, 31 | Files are opened using `open()` but not explicitly closed, which can lead to resource leaks and unexpected behavior. | Refactor `loadData` and `saveData` to use `with open(...) as f:` to ensure files are automatically closed. |
| **Old-style string formatting** | Pylint | Convention (`C0209`) | 14 | Uses `%` operator for string formatting, which is less readable and flexible than f-strings or `.format()`. | Convert to an f-string: `f"{datetime.now()}: Added {qty} of {item}"`. |
| **Global variable access/modification** | Pylint | Warning (`W0603`) | 27, 28 | `stock_data` is modified as a global variable. While sometimes necessary, it can make code harder to reason about and test. | (For this lab, we'll note it but keep it, as a full refactor to a class is beyond scope). |
| **Function name convention (`snake_case`)** | Pylint | Convention (`C0103`) | Many | Functions like `addItem`, `removeItem`, `getQty` do not follow Python's `snake_case` naming convention. | Rename functions to `add_item`, `remove_item`, `get_qty`, etc. |
| **Undefined variable (`i`)** | Flake8 | Error (`F821`) | 62 | The variable `i` is used in `printData` without being explicitly defined or unpacked. | Iterate directly over `stock_data.items()` to get both key and value: `for item, quantity in stock_data.items():`. |
| **Line too long** | Flake8 | Error (`E501`) | (various) | Some lines exceed the recommended 79/80 character limit, reducing readability. | Refactor long lines, split strings, or break up complex expressions. |

---

## Reflections

### 1. Easiest vs. Hardest Fixes

* **Easiest:**
    * Flake8 issues like "line too long" (E501) and function naming conventions (C0103 from Pylint, though Flake8 might also have style checks) are generally straightforward to fix, often just requiring reformatting or renaming.
    * Replacing old `%` string formatting with f-strings is also quick.
    * Removing the `eval()` call is simple once identified, as it's often a direct removal or a simple replacement if its functionality was non-malicious.
* **Hardest:**
    * **Mutable Default Argument (`logs=[]`):** This is a subtle logical bug that doesn't immediately crash but causes unexpected behavior. Understanding *why* it's a problem and implementing the `if logs is None: logs = []` pattern requires a deeper understanding of Python's object model.
    * **Handling `KeyError` safely in `removeItem` and `getQty`:** While the fix (using `dict.get()` or a `try-except KeyError`) is relatively simple, accurately identifying *all* places where a `KeyError` could occur and deciding on the best handling strategy (return 0, log a warning, raise a specific error) requires careful thought about the function's contract.
    * **Refactoring global variable use:** While not strictly *required* to fix all warnings, a more robust solution would involve refactoring `stock_data` into a class, which is a larger architectural change.

### 2. False Positives

* In this specific code and with these tools, there weren't many obvious "false positives" in terms of critical issues. Most warnings pointed to real problems or areas for improvement.
* *Potential examples of false positives in general scenarios:*
    * A linter might flag a variable as "unused" if it's only used within a complex context (e.g., in a list comprehension that's passed to another function), but the linter's static analysis can't fully trace its use.
    * Bandit might flag certain uses of `subprocess.call` or `os.system` as high severity (`B603`, `B607`), even if the arguments passed are hardcoded and not derived from user input, making them safe in that specific context.
    * Pylint might give a `too-many-arguments` warning (R0913) for a perfectly legitimate function, requiring a `# pylint: disable=too-many-arguments` comment.

### 3. Integrating Static Analysis

I would integrate these static analysis tools into my development workflow at two main stages:

1.  **Local Development Environment (IDE Integration):**
    * Install Pylint, Flake8, and Bandit extensions in VS Code. This provides immediate, real-time feedback (e.g., squiggly lines under problematic code) as I write. This allows for quick, iterative fixes for style, syntax, and obvious security vulnerabilities before even running the code or committing.
    * Set up pre-commit hooks using tools like `pre-commit` to automatically run linters and formatters before code is committed. This ensures consistent code style and basic quality checks across the team.

2.  **Continuous Integration (CI) Pipeline:**
    * Incorporate these tools into the CI pipeline (e.g., GitHub Actions, Jenkins, GitLab CI). Every time a pull request is opened or code is pushed to a feature branch, the CI would run the static analysis tools.
    * Set up rules to fail the build or PR check if high-severity issues (like Bandit's `B307` for `eval`) are found, or if the Pylint score drops below a certain threshold. This acts as a quality gate, preventing problematic code from merging into the main branch and providing an objective code quality metric for team reviews.

### 4. Observed Improvements

After applying the fixes based on these reports, I anticipate the following significant improvements:

* **Increased Robustness and Stability:** Addressing issues like mutable default arguments, bare `except` blocks, and unsafe dictionary access (`getQty`) will prevent unexpected runtime errors and ensure the program behaves predictably, even with unusual inputs or edge cases.
* **Enhanced Security:** Removing the `eval()` call is a critical security improvement, eliminating a major potential attack vector for arbitrary code execution.
* **Improved Code Quality and Maintainability:**
    * Using `with open(...)` ensures proper resource management, preventing file handle leaks.
    * Consistent naming conventions (`snake_case`) and better string formatting (`f-strings`) make the code easier to read, understand, and maintain for anyone working on it.
    * Addressing "line too long" improves readability, especially on smaller screens or in side-by-side diffs during code reviews.
* **Reduced Debugging Time:** By catching potential bugs and vulnerabilities early during static analysis, developers save significant time that would otherwise be spent debugging runtime errors later. The code will also be cleaner, making logical flaws easier to spot.