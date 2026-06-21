import sqlite3 as x

DB_NAME = "expenses.db"


def Create_DB():
    conn = x.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        amount REAL NOT NULL CHECK(amount > 0),
        category TEXT NOT NULL,
        description TEXT
    )
    """)

    conn.commit()
    conn.close()


def expense_add(date, amount, category, desc):
    if amount <= 0:
        print("Amount must be greater than 0!")
        return

    conn = x.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO expenses(date, amount, category, description)
    VALUES (?, ?, ?, ?)
    """, (date, amount, category, desc))

    conn.commit()
    conn.close()


def expense_view_all():
    conn = x.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT * FROM expenses")
    records = cur.fetchall()

    conn.close()
    return records

def expense_exists(expense_id):
    conn = x.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM expenses WHERE id = ?",
        (expense_id,)
    )

    result = cur.fetchone()

    conn.close()

    return result is not None

def delete_expense(expense_id):
    conn = x.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    deleted = cur.rowcount

    conn.commit()
    conn.close()

    return deleted > 0


def edit_expense(expense_id, new_date, new_amount, new_category, new_desc):
    if new_amount <= 0:
        print("Amount must be greater than 0!")
        return

    conn = x.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    UPDATE expenses
    SET date = ?,
        amount = ?,
        category = ?,
        description = ?
    WHERE id = ?
    """, (new_date, new_amount, new_category, new_desc, expense_id))

    conn.commit()
    conn.close()


def drop_database():
    conn = x.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS expenses")

    conn.commit()
    conn.close()


def total_expenses():
    conn = x.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT SUM(amount) FROM expenses")
    total = cur.fetchone()[0]

    conn.close()

    if total is None:
        return 0

    return total


def expense_by_category():
    conn = x.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    SELECT category, SUM(amount)
    FROM expenses
    GROUP BY category
    """)

    data = cur.fetchall()

    conn.close()
    return data
def expense_by_category():
    conn = x.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    data = cur.fetchall()

    conn.close()
    return data