# Personal Expense Tracker

A command-line expense tracking application built with Python and SQLite, featuring a color-coded terminal interface and visual spending analytics.

---

## About

This project was built by **Iraj Mudgal**, a Mechanical Engineering student at MIT Manipal, as a personal summer project undertaken to refine his programming skills outside of coursework.

---

## Overview

Personal Expense Tracker is a lightweight, terminal-based application that allows a user to record, manage, and analyze daily expenses. It combines a persistent SQLite backend with the Rich library for a clean console UI, and uses Matplotlib to visualize spending habits through pie charts.

This project was built as a hands-on exercise in:
- Structuring a Python application with separation of concerns (UI layer vs. data layer)
- Performing CRUD operations using `sqlite3`
- Building interactive CLI menus
- Data visualization with `matplotlib`

---

## Features Explained

### 1. Add Expense
Lets the user record a new expense by entering a date, amount, category, and description. The amount is validated to ensure it is a positive number before being inserted into the database; invalid or non-numeric input is caught and reported back to the user instead of crashing the program.

### 2. View All Expenses
Fetches every record from the `expenses` table and displays it as a formatted table (built with Rich's `Table` class), with separate color-coded columns for ID, Date, Amount, Category, and Description. If no records exist, the user is informed instead of being shown an empty table.

### 3. Delete Expense
Prompts the user for an expense ID and removes the matching row from the database. The function checks how many rows were actually affected (`cur.rowcount`) so it can correctly report whether the deletion succeeded or whether that ID didn't exist.

### 4. Drop Database
A destructive action that clears every expense record by dropping and recreating the `expenses` table. Because this is irreversible, the program requires the user to type "yes" to confirm before proceeding, reducing the chance of accidental data loss.

### 5. Edit Expense
Allows the user to update an existing record (date, amount, category, description) by ID. Like the Add Expense feature, the new amount is validated to be greater than zero before the update is committed.

### 6. Show Total Expenses
Runs a `SUM(amount)` query across the entire table and displays the cumulative total. If the table is empty, the function safely returns 0 instead of `None`, avoiding a crash when formatting the output.

### 7. Expense Pie Chart
Groups all expenses by category using a `GROUP BY` SQL query, then passes the resulting category totals into Matplotlib to render a pie chart. Each slice represents a category's share of total spending, with percentage labels for quick visual comparison.

### 8. Exit
Cleanly breaks out of the main application loop and ends the program with a closing message.

### Input Validation (cross-cutting)
Every menu option that accepts numeric input (amount, expense ID) is wrapped in a `try/except ValueError` block, so the program never crashes from a typo or invalid entry -- it simply reports the error and lets the user try again.

---

## Tech Stack and How Each Tool Is Used

### Python (`sqlite3` module)
The application's data layer (`database.py`) uses Python's built-in `sqlite3` module to talk directly to a local `expenses.db` file. Every function follows the same pattern: open a connection, run a query with parameterized placeholders (`?`) to prevent SQL injection, commit if needed, and close the connection. No external database server is required, which makes the app portable and easy to run with zero setup.

### Rich
Rich is used purely in `main.py` for the presentation layer. It provides:
- `Console()` for colored, styled print statements (e.g., green for success, red for errors, yellow for warnings)
- `console.rule()` to draw the title banner
- `Table` to render query results as a clean, aligned table directly in the terminal, instead of printing raw tuples

Rich has no awareness of the database; it only ever receives plain Python data (lists, strings, numbers) that `database.py` returns.

### Matplotlib
Matplotlib is used for the one visual feature in the app: the expense pie chart. The category totals returned by `expense_by_category()` are split into two lists (`categories` and `amounts`) and passed to `plt.pie()`. This is the only place in the project where data leaves the terminal and is shown in a separate graphical window.

### Why this separation matters
Because `database.py` only returns plain data (lists of tuples, numbers) and never touches Rich or Matplotlib directly, either of those libraries could be swapped out or removed without changing a single line of the database code. This is a basic but important software design principle: keeping the data layer independent of the presentation layer.

---

## Adapting This Project to MySQL

The project currently uses SQLite because it requires no separate server and stores everything in a single local file, which is ideal for a personal CLI tool. However, the same logic can be adapted to use MySQL (or any other relational database) with a fairly small set of changes, since the SQL syntax used here is simple and largely portable.

### What would need to change

1. Driver/library
   Replace the built-in `sqlite3` import with a MySQL driver such as `mysql-connector-python` or `PyMySQL`:
   ```bash
   pip install mysql-connector-python
   ```
   ```python
   import mysql.connector as x
   ```

2. Connection details
   `sqlite3.connect(DB_NAME)` only needs a filename. MySQL needs a host, user, password, and database name:
   ```python
   def get_connection():
       return x.connect(
           host="localhost",
           user="your_username",
           password="your_password",
           database="expense_tracker"
       )
   ```
   Every function in `database.py` would call `get_connection()` instead of `x.connect(DB_NAME)`.

3. AUTOINCREMENT syntax
   SQLite uses `INTEGER PRIMARY KEY AUTOINCREMENT`. MySQL uses a different keyword:
   ```sql
   CREATE TABLE IF NOT EXISTS expenses (
       id INT AUTO_INCREMENT PRIMARY KEY,
       date DATE NOT NULL,
       amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
       category VARCHAR(100) NOT NULL,
       description TEXT
   )
   ```
   Note that `REAL` is also better represented as `DECIMAL(10,2)` in MySQL for accurate currency handling, and `TEXT` for the date column is better stored as a proper `DATE` type.

4. Placeholder style
   SQLite uses `?` as a parameter placeholder; MySQL connectors typically use `%s`:
   ```python
   cur.execute("INSERT INTO expenses(date, amount, category, description) VALUES (%s, %s, %s, %s)",
               (date, amount, category, desc))
   ```

5. Database creation
   SQLite creates the `.db` file automatically on first connection. With MySQL, the database itself (`expense_tracker`) must already exist on the server before the table can be created, either created manually once via a MySQL client or with a `CREATE DATABASE IF NOT EXISTS expense_tracker` statement run separately.

6. Everything else stays the same
   The actual function signatures, the Rich table rendering, and the Matplotlib pie chart logic in `main.py` would not need to change at all, since they only depend on the data returned (lists of tuples), not on which database produced it. This is the direct benefit of having kept the database logic isolated in `database.py`.

In short: moving to MySQL is mostly a matter of changing the connection setup, the table-creation syntax, and the parameter placeholder style. The overall structure and the rest of the application logic remains unchanged.

---

## Tech Stack Summary

- Language: Python 3
- Database: SQLite3 (via Python's built-in `sqlite3` module)
- Terminal UI: `rich` -- for tables, colors, and formatted console output
- Visualization: `matplotlib` -- for pie chart generation

---

## Project Structure

```
expense-tracker/
|
|-- main.py          Application entry point -- CLI menu and user interaction loop
|-- database.py       Data access layer -- all SQLite operations (CRUD)
|-- expenses.db        SQLite database file (auto-generated on first run)
```

### Architecture

The project follows a simple two-layer design:

- `database.py` handles all direct interaction with the SQLite database: creating tables, inserting, updating, deleting, and querying records. No UI logic lives here.
- `main.py` handles the presentation layer: rendering the menu, capturing user input, validating it, and calling the appropriate `database.py` functions.

This separation keeps the persistence logic independent of the interface, making the database layer reusable -- it could later be connected to MySQL, a GUI, or a web frontend with minimal changes to `main.py`.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps

1. Clone the repository
   ```bash
   git clone https://github.com/<your-username>/expense-tracker.git
   cd expense-tracker
   ```

2. Install dependencies
   ```bash
   pip install rich matplotlib
   ```

3. Run the application
   ```bash
   python main.py
   ```

   On first run, `expenses.db` will be created automatically in the project directory.

---

## Usage

Upon launching, the main menu is displayed:

```
====================================================================================================
--------------------------------------- PERSONAL EXPENSE TRACKER ---------------------------------
====================================================================================================
[1]  Add Expense
[2]  View All Expenses
[3]  Delete Expense
[4]  Drop Database
[5]  Edit Expense
[6]  Show Total Expenses
[7]  Expense Pie Chart
[0]  Exit

Enter your choice:
```

Enter the number corresponding to the desired action and follow the on-screen prompts.

### Example: Adding an Expense
```
Enter your choice: 1
Enter Date (YYYY-MM-DD): 2026-06-21
Enter Amount: 450
Enter Category: Groceries
Enter Description: Weekly vegetables and milk
Expense Added Successfully!
```

### Example: Viewing the Pie Chart
Selecting option 7 opens a Matplotlib window showing total spend broken down by category, with each slice labeled and its percentage share displayed.

---

## Database Schema

The application uses a single table, `expenses`, defined as follows:

| Column      | Type    | Constraints                      |
|-------------|---------|-----------------------------------|
| id          | INTEGER | PRIMARY KEY, AUTOINCREMENT        |
| date        | TEXT    | NOT NULL                          |
| amount      | REAL    | NOT NULL, CHECK(amount > 0)       |
| category    | TEXT    | NOT NULL                          |
| description | TEXT    | --                                 |

---

## Function Reference (database.py)

| Function | Purpose |
|---|---|
| Create_DB() | Creates the expenses table if it doesn't already exist |
| expense_add(date, amount, category, desc) | Inserts a new expense record |
| expense_view_all() | Retrieves all expense records |
| expense_exists(expense_id) | Checks whether a given expense ID exists |
| delete_expense(expense_id) | Deletes an expense by ID; returns True/False based on success |
| edit_expense(expense_id, ...) | Updates an existing expense's fields |
| drop_database() | Drops the expenses table entirely |
| total_expenses() | Returns the sum of all recorded amounts |
| expense_by_category() | Returns total spend grouped by category (used for the pie chart) |

---

## Future Improvements

- Add monthly/yearly filtering and reports
- Export records to CSV/PDF
- Add a budget-limit warning system
- Migrate to MySQL or PostgreSQL for multi-device/multi-user support
- Migrate to a GUI (Tkinter/PyQt) or web interface (Flask/Streamlit)
- Add unit tests for the database layer
- Support multiple currencies

---

## Author

Iraj Mudgal
Mechanical Engineering Student, MIT Manipal

Built independently as a personal summer project to practice Python, SQLite, and CLI application design.
