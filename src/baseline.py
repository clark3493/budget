import pathmagic
from table import Field, FieldConstraint, Table, TableConstraint
    
# EXPENSE CATEGORY TABLE
table_expense_category = Table(
    "ExpenseCategory",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Name","TEXT",constraints="NOT NULL"),
               Field("Created","TIMESTAMP",constraints="NOT NULL")
               ]
    )
    
# EXPENSE SUBCATEGORY TABLE
table_expense_subcategory = Table(
    "ExpenseSubCategory",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Name","TEXT",constraints="NOT NULL"),
               Field("ParentCategory","INTEGER",constraints="NOT NULL"),
               Field("Created","TIMESTAMP",constraints="NOT NULL")
               ],
    constraints = TableConstraint("FOREIGN KEY", "ParentCategory", "ExpenseCategory(ID)")
    )
    
# PAYMENT TYPE TABLE
table_payment_type = Table(
    "PaymentType",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Name","TEXT",constraints="NOT NULL"),
               Field("Created","TIMESTAMP",constraints="NOT NULL")
               ]
    )
    
# ACCOUNT
table_account = Table(
    "Account",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Name","TEXT",constraints="NOT NULL"),
               Field("Balance","REAL",constraints="NOT NULL"),
               Field("Created","TIMESTAMP",constraints="NOT NULL")
               ]
    )
    
# EXPENSE RECIPIENT
table_expense_recipient = Table(
    "ExpenseRecipient",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Name","TEXT",constraints="NOT NULL"),
               Field("Created","TIMESTAMP",constraints="NOT NULL")
               ]
    )
    
# EXPENSE RECIPIENT ALIAS
table_expense_recipient_alias = Table(
    "ExpenseRecipientAlias",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Recipient","INTEGER",constraints="NOT NULL"),
               Field("Alias","TEXT",constraints="NOT NULL"),
               Field("AliasType","TEXT"),
               Field("Created","TIMESTAMP",constraints="NOT NULL")
               ],
    constraints = [ TableConstraint("FOREIGN KEY","Recipient","ExpenseRecipient(ID)") ]
    )

# EXPENSE TABLE
table_expense = Table(
    "Expense",
    fields = [ Field("ID", "INTEGER",constraints=["PRIMARY KEY", "NOT NULL"]),
               Field("Value", "REAL",constraints="NOT NULL"),
               Field("Account", "INTEGER",constraints="NOT NULL"),
               Field("Date", "DATE"),
               Field("Category", "INTEGER"),
               Field("SubCategory", "INTEGER"),
               Field("Flag", "INTEGER"),
               Field("PaymentType", "INTEGER"),
               Field("PaidTo", "INTEGER"),
               Field("Created", "TIMESTAMP", constraints="NOT NULL")
               ],
    constraints = [ TableConstraint("FOREIGN KEY", "Account", "Account(ID)"),
                    TableConstraint("FOREIGN KEY", "Category", "ExpenseCategory(ID)"),
                    TableConstraint("FOREIGN KEY", "SubCategory", "ExpenseSubCategory(ID)"),
                    TableConstraint("FOREIGN KEY", "PaymentType", "PaymentType(ID)"),
                    TableConstraint("FOREIGN KEY", "PaidTo", "ExpenseRecipient(ID)")
                    ]
    )
    
# INCOME CATEGORY TABLE
table_income_category = Table(
    "IncomeCategory",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Name","TEXT",constraints="NOT NULL"),
               Field("Created","TIMESTAMP",constraints="NOT NULL")
               ]
    )
    
# INCOME SUBCATEGORY TABLE
table_income_subcategory = Table(
    "IncomeSubCategory",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Name","TEXT",constraints="NOT NULL"),
               Field("ParentCategory","INTEGER",constraints="NOT NULL"),
               Field("Created","TIMESTAMP",constraints="NOT NULL")
               ],
    constraints=TableConstraint("FOREIGN KEY", "ParentCategory", "IncomeCategory(ID)")
    )
    
# INCOME SOURCE
table_income_source = Table(
    "IncomeSource",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Name","TEXT",constraints="NOT NULL"),
               Field("Created","TIMESTAMP",constraints="NOT NULL")
               ]
    )
    
# INCOME TABLE
table_income = Table(
    "Income",
    fields = [ Field("ID","INTEGER",constraints=["PRIMARY KEY","NOT NULL"]),
               Field("Value","REAL",constraints="NOT NULL"),
               Field("Account","INTEGER",constraints="NOT NULL"),
               Field("Date","DATE"),
               Field("Category","INTEGER"),
               Field("SubCategory","INTEGER"),
               Field("Source","INTEGER"),
               Field("Created","TIMESTAMP",constraints="NOT NULL")
               ],
    constraints = [ TableConstraint("FOREIGN KEY","Account","Account(ID)"),
                    TableConstraint("FOREIGN KEY","Category","IncomeCategory(ID)"),
                    TableConstraint("FOREIGN KEY","SubCategory","IncomeSubCategory(ID)"),
                    TableConstraint("FOREIGN KEY","Source","IncomeSource(ID)")
                    ]
    )
    
def baseline_tables():
    return [ table_expense_category,
             table_expense_subcategory,
             table_payment_type,
             table_account,
             table_expense_recipient,
             table_expense_recipient_alias,
             table_expense,
             table_income_category,
             table_income_subcategory,
             table_income_source,
             table_income
             ]