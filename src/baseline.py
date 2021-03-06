import pathmagic
from table import Field, FieldConstraint, Table, TableConstraint
    

# ACCOUNT TABLE
table_account = Table(
    'Account',
    fields=[Field('ID', 'INTEGER', constraints=['PRIMARY KEY', 'NOT NULL']),
            Field('Name', 'TEXT', 'NOT NULL'),
            Field('Type', 'TEXT'),
            Field('StartBalance', 'REAL', 'NOT NULL'),
            Field('Created', 'TIMESTAMP')]
)

# ACCOUNT - ATTRIBUTE INTERMEDIATE TABLE
table_account_attribute = Table(
    'AccountAttribute',
    fields=[Field('AccountID', 'INTEGER', 'NOT NULL'),
            Field('AttributeID', 'INTEGER', 'NOT NULL')],
    constraints=[TableConstraint('FOREIGN KEY', 'AccountID', 'Account(ID)'),
                 TableConstraint('FOREIGN KEY', 'AttributeID', 'Attribute(ID)')]
)

# ALIAS TABLE
table_alias = Table(
    'Alias',
    fields=[Field('ID', 'INTEGER', constraints=['PRIMARY KEY', 'NOT NULL']),
            Field('Account', 'INTEGER', 'NOT NULL'),
            Field('String', 'TEXT', 'NOT NULL'),
            Field('Type', 'TEXT'),
            Field('Created', 'TIMESTAMP', 'NOT NULL'),
            Field('Modified', 'TIMESTAMP')],
    constraints=TableConstraint('FOREIGN KEY', 'Account', 'Account(ID)')
)

# ATTRIBUTE TABLE
table_attribute = Table(
    'Attribute',
    fields=[Field('ID', 'INTEGER', constraints=['PRIMARY KEY', 'NOT NULL']),
            Field('Name', 'TEXT', 'NOT NULL'),
            Field('Created', 'TIMESTAMP', 'NOT NULL')]
)

# CATEGORY TABLE
table_category = Table(
    'Category',
    fields=[Field('ID', 'INTEGER', constraints=['PRIMARY KEY', 'NOT NULL']),
            Field('Name', 'TEXT', constraints=['NOT NULL', 'UNIQUE']),
            Field('Created', 'TIMESTAMP', 'NOT NULL')]
)

# SUB CATEGORY TABLE
table_subcategory = Table(
    'SubCategory',
    fields=[Field('ID', 'INTEGER', constraints=['PRIMARY KEY', 'NOT NULL']),
            Field('Name', 'TEXT', 'NOT NULL'),
            Field('Parent', 'INTEGER', 'NOT NULL'),
            Field('Created', 'TIMESTAMP', 'NOT NULL')],
    constraints=TableConstraint('FOREIGN KEY', 'Parent', 'Category(ID)')
)

# TRANSACTION TABLE
table_transaction = Table(
    'Transactions',
    fields=[Field('ID', 'INTEGER', constraints=['PRIMARY KEY', 'NOT NULL']),
            Field('Value', 'REAL', 'NOT NULL'),
            Field('FromAccount', 'INTEGER'),
            Field('ToAccount', 'INTEGER'),
            Field('TransactionType', 'TEXT'),
            Field('Date', 'DATE'),
            Field('Description', 'TEXT'),
            Field('Category', 'INTEGER'),
            Field('SubCategory', 'INTEGER'),
            Field('PaymentType', 'TEXT'),
            Field('Created', 'TIMESTAMP', 'NOT NULL'),
            Field('Modified', 'TIMESTAMP')],
    constraints=[TableConstraint('FOREIGN KEY', 'FromAccount', 'Account(ID)'),
                 TableConstraint('FOREIGN KEY', 'ToAccount', 'Account(ID)'),
                 TableConstraint('FOREIGN KEY', 'Category', 'Category(ID)'),
                 TableConstraint('FOREIGN KEY', 'SubCategory', 'SubCategory(ID)'),
                 TableConstraint('CHECK', 'NOT(FromAccount IS NULL AND ToAccount IS NULL)'),
                 TableConstraint('CHECK', 'NOT(Category IS NULL AND SubCategory IS NOT NULL)')]
)

# TRANSACTION - CATEGORY INTERMEDIATE TABLE
table_transaction_category = Table(
    'TransactionCategory',
    fields=[Field('TransactionID', 'INTEGER', 'NOT NULL'),
            Field('CategoryID', 'INTEGER', 'NOT NULL')],
    constraints=[TableConstraint('FOREIGN KEY', 'TransactionID', 'Transactions(ID)'),
                 TableConstraint('FOREIGN KEY', 'CategoryID', 'Category(ID)')]
)

# TRANSACTION - SUBCATEGORY INTERMEDIATE TABLE
table_transaction_subcategory = Table(
    'TransactionSubCategory',
    fields=[Field('TransactionID', 'INTEGER', 'NOT NULL'),
            Field('SubCategoryID', 'INTEGER', 'NOT NULL')],
    constraints=[TableConstraint('FOREIGN KEY', 'TransactionID', 'Transactions(ID)'),
                 TableConstraint('FOREIGN KEY', 'SubCategoryID', 'SubCategory(ID)')]
)


def baseline_tables():
    return [table_account,
            table_account_attribute,
            table_alias,
            table_attribute,
            table_category,
            table_subcategory,
            table_transaction,
            table_transaction_category,
            table_transaction_subcategory]
