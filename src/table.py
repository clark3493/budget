
class Field(object):

    VALID_TYPES = ['BLOB',
                   'DATE',
                   'INTEGER',
                   'NUMERIC',
                   'REAL',
                   'TEXT',
                   'TIMESTAMP']

    def __init__(self, name, data_type, constraints=None):

        # input error handling
        if type(name) is not str or type(data_type) is not str:
            raise TypeError('name and data_type input to Field object must be strings')

        if data_type.upper() not in Field.VALID_TYPES:
            msg  = "'{}' is not a valid data type\n".format(data_type)
            msg += "    Valid data type are: {}".format(Field.VALID_TYPES)
            raise ValueError(msg)

        if constraints is not None:
            if type(constraints) is not list:
                constraints = [constraints]
            for i,cstr in enumerate(constraints):
                if not isinstance(cstr, FieldConstraint) and cstr not in FieldConstraint.VALID_SOLO_CONSTRAINTS:
                    raise ValueError("{} is not a valid constraint".format(cstr))
                elif not isinstance(cstr, FieldConstraint):
                    constraints[i] = FieldConstraint(cstr)

        # define the field
        self.name = name
        self.dtype = data_type.upper()
        self.constraints = constraints

    def write(self):
        sql_string = self.name + ' ' + self.dtype
        if self.constraints is not None:
            for cstr in self.constraints:
                sql_string += ' ' + cstr.write()

        return sql_string


class FieldConstraint(object):

    VALID_CONSTRAINTS = ['CHECK',
                         'DEFAULT',
                         'FOREIGN KEY',
                         'NOT NULL',
                         'PRIMARY KEY',
                         'UNIQUE']

    VALID_SOLO_CONSTRAINTS = ['NOT NULL',
                              'PRIMARY KEY',
                              'UNIQUE']

    def __init__(self, constraint, *args):
        if constraint.upper() not in FieldConstraint.VALID_CONSTRAINTS:
            raise ValueError("{} is not a valid field constraint type".format(constraint))

        if constraint.upper() not in FieldConstraint.VALID_SOLO_CONSTRAINTS and not args:
            raise ValueError("CHECK, COLLATE, DEFAULT and FOREIGN KEY constraints require an additional argument")

        self.type = constraint.upper()
        if type(args) is tuple:
            self.args = args
        else:
            self.args = (args,)

    def write(self):
        if self.type in FieldConstraint.VALID_SOLO_CONSTRAINTS:
            return self.type
        elif self.type == 'CHECK':
            return self.type + '(' + str(self.args[0]) + ')'
        elif self.type == 'DEFAULT':
            return self.type + ' ' + str(self.args[0])
        else:
            raise ValueError("Constraint type '{}' not recognized".format(self.type))


class Table(object):

    def __init__(self, name, fields=None, constraints=None):
        # input error checking
        if type(name) is not str:
            raise TypeError("name input to Table object must be a string")

        if fields is not None:
            if type(fields) is list:
                for fld in fields:
                    if not isinstance(fld, Field):
                        raise TypeError("fields input to Table object must be a Field or list of Field objects")
            elif not isinstance(fields, Field):
                raise TypeError("fields input to Table object must be a Field or list of Field objects")

        if constraints is not None:
            if type(constraints) is list:
                for cstr in constraints:
                    if not isinstance(cstr, TableConstraint) and cstr not in TableConstraint.VALID_SOLO_CONSTRAINTS:
                        raise ValueError("{} is not a valid constraint".format(cstr))
            else:
                if not isinstance(constraints, TableConstraint) and constraints not in TableConstraint.VALID_SOLO_CONSTRAINTS:
                    raise ValueError("{} is not a valid constraint".format(constraints))

        # define the table
        self.name = name

        if type(fields) is list or fields is None:
            self.fields = fields
        else:
            self.fields = [fields]

        if type(constraints) is list or constraints is None:
            self.constraints = constraints
        else:
            self.constraints = [constraints]

    def create_cmd(self, if_not_exists=True, without_rowid=False):
        # CREATE TABLE [IF NOT EXISTS] name(
        cmd = "CREATE TABLE "
        if if_not_exists:
            cmd += "IF NOT EXISTS "
        cmd += self.name + "(\n"

        # FIELDS
        for i, fld in enumerate(self.fields):
            if i == len(self.fields)-1 and self.constraints is None:
                cmd += "    " + fld.write() + "\n"
            else:
                cmd += "    " + fld.write() + ",\n"

        # TABLE CONSTRAINTS
        if self.constraints is not None:
            for i, cstr in enumerate(self.constraints):
                if i == len(self.constraints)-1:
                    cmd += "    " + cstr.write() + "\n"
                else:
                    cmd += "    " + cstr.write() + ",\n"

        # ) [WITHOUT_ROWID];
        cmd += ")"
        if without_rowid:
            cmd += " WITHOUT_ROWID"
        cmd += ";"

        return cmd


class TableConstraint(object):
    VALID_CONSTRAINTS = ["CHECK",
                         "DEFAULT",
                         "FOREIGN KEY",
                         "NOT NULL",
                         "PRIMARY KEY",
                         "UNIQUE"]

    def __init__(self, constraint, *args):
        if constraint.upper() not in TableConstraint.VALID_CONSTRAINTS:
            raise ValueError("{} is not a valid field constraint type".format(constraint))

        if not args:
            raise ValueError("Table level constraints require additional arguments")

        self.type = constraint.upper()
        if type(args) is tuple:
            self.args = args
        else:
            self.args = (args,)

    def write(self):
        if self.type in ['CHECK', 'DEFAULT', 'NOT NULL', 'PRIMARY KEY', 'UNIQUE']:
            cmd = self.type + " " + str(self.args[0])
        elif self.type == 'FOREIGN KEY':
            cmd = self.type + "(" + str(self.args[0]) + ") REFERENCES " + str(self.args[1])
        else:
            raise ValueError("Constraint type '{}' not recognized".format(self.type))

        return cmd
