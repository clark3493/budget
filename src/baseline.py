from src.table import Field, Table

# EXPENSE TABLE
table_expense = Table(
    "Expense",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
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
    
# EXPENSE CATEGORY TABLE
table_expense_category = Table(
    "ExpenseCategory",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Name","TEXT",constraints="NOT NULL")
               ]
    )
    
# EXPENSE SUBCATEGORY TABLE
table_expense_subcategory = Table(
    "ExpenseSubCategory",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Name","TEXT",constraints="NOT NULL")
               ]
    )
    
# PAYMENT TYPE TABLE
table_payment_type = Table(
    "PaymentType",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Name","TEXT",constraints="NOT NULL")
               ]
    )
    
# ACCOUNT
table_account = Table(
    "Account",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Name","TEXT",constraints="NOT NULL"),
               Field("Balance","REAL",constraints="NOT NULL")
               ]
    )
    
# EXPENSE RECIPIENT
table_expense_recipient = Table(
    "ExpenseRecipient",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Name","TEXT",constraints="NOT NULL")
               ]
    )
    
# INCOME TABLE
table_income = Table(
    "Income",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Value","REAL",constraints="NOT NULL"),
               Field("BudgetMonth","TEXT",constraints="NOT NULL"),
               Field("BudgetYear","INTEGER",constraints="NOT NULL"),
               Field("PaymentAccount","TEXT",constraints="NOT NULL"),
               Field("Date","TEXT"),
               Field("IncomeCategory","TEXT"),
               Field("IncomeSubCategory","TEXT"),
               Field("IncomeSource","TEXT")
               ]
    )
    
# INCOME CATEGORY TABLE
table_income_category = Table(
    "IncomeCategory",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Name","TEXT",constraints="NOT NULL")
               ]
    )
    
# INCOME SUBCATEGORY TABLE
table_income_subcategory = Table(
    "IncomeSubCategory",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Name","TEXT",constraints="NOT NULL")
               ]
    )
    
# INCOME SOURCE
table_income_source = Table(
    "IncomeSource",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Name","TEXT",constraints="NOT NULL")
               ]
    )
    
def baseline_tables():
    return [ table_expense,
             table_expense_Category,
             table_expense_subcategory,
             table_payment_type,
             table_account,
             table_expense_recipient,
             table_income,
             table_income_category,
             table_income_subcategory,
             table_income_source
             ]