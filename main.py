from fastmcp import FastMCP
import os 
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
print(DB_PATH)

mcp = FastMCP(name="ExpenseTracker")

def init_db():
  with sqlite3.connect(DB_PATH) as conn:
    conn.execute("""
      CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        subcategory TEXT DEFAULT '',
        note TEXT DEFAULT ''
      )
    """)

init_db()

@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
  """
  Add a new expense to the database.

  Args:
      date (str): date of expense in format "YYYY-MM-DD"
      amount (float): amount of expense
      category (str): category of expense
      subcategory (str, optional): subcategory of expense, defaults to ""
      note (str, optional): note about expense, defaults to ""

  Returns:
      dict: with keys "status" and "id"
  """
  with sqlite3.connect(DB_PATH) as conn:
    cur = conn.execute("""
      INSERT INTO expenses (date, amount, category, subcategory, note)
      VALUES (?, ?, ?, ?, ?)
    """, (date, amount, category, subcategory, note))
    return {"status": "ok", "id": cur.lastrowid}
  
@mcp.tool()
def list_expenses(start_date=None, end_date=None):
  """
  List all expenses in the database.

  Args:
      start_date (str, optional): start date of expenses in format "YYYY-MM-DD", defaults to None
      end_date (str, optional): end date of expenses in format "YYYY-MM-DD", defaults to None

  Returns:
      list of dicts: each dict represents an expense with keys "id", "date", "amount", "category", "subcategory", "note"
  """
  with sqlite3.connect(DB_PATH) as conn:
    cur = conn.execute("""
        SELECT id as ID, 
        date as Date, 
        '₹' || amount as Amount, 
        category as Category, 
        subcategory as Subcategory, 
        note as Note 
        FROM expenses 
        WHERE date BETWEEN ? AND ?
        ORDER BY date DESC
        """, (start_date, end_date))
    cols = [col[0] for col in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]
  
@mcp.tool()
def summarize(start_date=None, end_date=None, category=None):
  """
  Summarize expenses by category.

  Args:
      start_date (str, optional): start date of expenses in format "YYYY-MM-DD", defaults to None
      end_date (str, optional): end date of expenses in format "YYYY-MM-DD", defaults to None
      category (str, optional): category of expenses, defaults to None

  Returns:
      dict: with keys "category" and "amount"
  """
  with sqlite3.connect(DB_PATH) as conn:
    cur = conn.execute("""
        SELECT category as Category, SUM(amount) as Amount 
        FROM expenses 
        WHERE date BETWEEN ? AND ? AND category = ?
        GROUP BY category
        """, (start_date, end_date, category))
    cols = [col[0] for col in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]
  
@mcp.resource("expense://categories", mime_type="application/json")
def get_categories():
  """
    Return a JSON string containing a list of categories.

    Returns:
        str: a JSON string containing a list of categories
  """
  with open("categories.json", "r") as f:
    return f.read()

# Start ther server
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)