from src.table import Constraint, Field, Table

table_expense = Table(
    "Expense",
    fields = [Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
              Field("Value","REAL",constraints="NOT NULL"),
              Field("BudgetMonth","TEXT",constraints="NOT NULL"),
              Field("BudgetYear","INTEGER",constraints="NOT NULL"),
              Field("PaymentAccount","TEXT",constraints="NOT NULL"),
              Field("Date","TEXT"),
              Field("ExpenseCategory","TEXT"),
              Field("ExpenseSubCategory","TEXT"),
              Field("PaymentType","TEXT"),
              Field("PaidTo","TEXT")
              ]
    )
    
def baseline_tables():
    return [ table_expense ]