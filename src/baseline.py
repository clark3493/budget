import pathmagic
from table import Field, FieldConstraint, Table, TableConstraint
    

# ACCOUNT TABLE
table_account = Table(
    'Account',
    fields=[Field('ID', 'INTEGER', constraints=['PRIMARY KEY', 'NOT NULL']),
            Field('Name', 'TEXT', 'NOT NULL'),
            Field('StartBalance', 'REAL', 'NOT NULL'),
            Field('StartDate', 'DATE', 'NOT NULL'),
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
            Field('SubCategoryID', 'INTEGER'),
            Field('MerchantID', 'INTEGER'),
            Field('String', 'TEXT', 'NOT NULL'),
            Field('Type', 'TEXT', 'NOT NULL'),
            Field('Created', 'TIMESTAMP', 'NOT NULL'),
            Field('Modified', 'TIMESTAMP')],
    constraints=[TableConstraint('FOREIGN KEY', 'SubCategoryID', 'SubCategory(ID)'),
                 TableConstraint('FOREIGN KEY', 'MerchantID', 'Merchant(ID)'),
                 TableConstraint('CHECK', 'NOT(SubCategoryID IS NULL AND MerchantID IS NULL)')]
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

# MERCHANT TABLE
table_merchant = Table(
    'Merchant',
    fields=[Field('ID', 'INTEGER', constraints=['PRIMARY KEY', 'NOT NULL']),
            Field('Name', 'TEXT', constraints=['NOT NULL', 'UNIQUE']),
            Field('Created', 'TIMESTAMP', 'NOT NULL')]
)

# SUB CATEGORY TABLE
table_subcategory = Table(
    'SubCategory',
    fields=[Field('ID', 'INTEGER', constraints=['PRIMARY KEY', 'NOT NULL']),
            Field('Name', 'TEXT', 'NOT NULL'),
            Field('ParentID', 'INTEGER', 'NOT NULL'),
            Field('Created', 'TIMESTAMP', 'NOT NULL')],
    constraints=TableConstraint('FOREIGN KEY', 'ParentID', 'Category(ID)')
)

# TRANSACTION TABLE
table_transaction = Table(
    'Transactions',
    fields=[Field('ID', 'INTEGER', constraints=['PRIMARY KEY', 'NOT NULL']),
            Field('Value', 'REAL', 'NOT NULL'),
            Field('FromAccountID', 'INTEGER'),
            Field('ToAccountID', 'INTEGER'),
            Field('TransactionType', 'TEXT'),
            Field('Date', 'DATE'),
            Field('Description', 'TEXT'),
            Field('PaymentType', 'TEXT'),
            Field('Created', 'TIMESTAMP', 'NOT NULL'),
            Field('Modified', 'TIMESTAMP')],
    constraints=[TableConstraint('FOREIGN KEY', 'FromAccountID', 'Account(ID)'),
                 TableConstraint('FOREIGN KEY', 'ToAccountID', 'Account(ID)')]
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
            table_merchant,
            table_subcategory,
            table_transaction,
            table_transaction_category,
            table_transaction_subcategory]
