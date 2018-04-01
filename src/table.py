
class Constraint(object):
    VALID_CONSTRAINTS = [ "CHECK",
                          "DEFAULT",
                          "FOREIGN KEY",
                          "NOT NULL",
                          "PRIMARY KEY",
                          "UNIQUE" ]
    
    # THIS WILL NEED TO BE MODIFIED, SOME CONSTRAINTS ARE DEFINED DIFFERENTLY
    # AT THE TABLE VS FIELD LEVEL
    SOLO_CONSTRAINTS  = [ "FOREIGN KEY",
                          "NOT NULL",
                          "PRIMARY KEY",
                          "UNIQUE" ]
                          
    def __init__(self,constraint,*args):
        if constraint not in Constraint.VALID_CONSTRAINTS:
            raise ValueError("{} is not a valid constraint type".format(constraint))
        
        self.type = constraint
        
        if constraint not in Constraint.SOLO_CONSTRAINTS and len(args) < 1:
            raise ValueError("DEFAULT and CHECK constraints require an additional argument")
        elif constraint not in Constraint.SOLO_CONSTRAINTS:
            self.arg = str(args[0])
            
    def write(self):
        if self.type in Constraint.SOLO_CONSTRAINTS:
            return self.type
        elif self.type == "DEFAULT":
            return self.type + " " + self.arg
        else:
            return self.type + "(" + self.arg + ")"
            
        

class Field(object):
    
    VALID_TYPES = [ "INTEGER",
                    "TEXT",
                    "BLOB",
                    "REAL",
                    "NUMERIC" ]

    def __init__(self,name,data_type,constraints=None):
        
        # input error handling
        if type(name) != str or type(data_type) != str:
            raise TypeError("name and data_type input to Field object must be a string")
            
        if data_type not in Field.VALID_TYPES:
            msg  = "'{}' is not a valid data type\n".format(data_type)
            msg += "            This Python implementation only supports entry of the 5 true sqlite3 data types\n"
            msg += "            Visit https://www.sqlite.org/datatype3.html for additional details\n"
            raise ValueError(msg)
            
        if constraints != None:
            if type(constraints) != list:
                constraints = [constraints]
            for i,cstr in enumerate(constraints):
                if not isinstance(cstr,Constraint) and cstr not in Constraint.SOLO_CONSTRAINTS:
                    raise ValueError("{} is not a valid constraint".format(cstr))
                elif not isinstance(cstr,Constraint):
                    constraints[i] = Constraint(cstr)
        
        # define the field        
        self.name = name
        self.dtype = data_type
        self.constraints = constraints
            
    def write(self):
        sql_string = self.name + " " + self.dtype
        if self.constraints != None:
            for cstr in self.constraints:
                sql_string += " " + cstr.write()
                
        return sql_string
        

class Table(object):
    def __init__(self, name, fields=None, constraints=None):
        # input error checking
        if type(name) != str:
            raise TypeError("name input to Table object must be a string")
        
        if fields != None:
            if type(fields) == list:
                for fld in fields:
                    if not isinstance(fld,Field):
                        raise TypeError("fields input to Table object must be a Field or list of Field objects")
            elif not isinstance(fld,Field):
                raise TypeError("fields input to Table object must be a Field or list of Field objects")
        
        # THIS WILL NEED TO BE UPDATED, PRIMARY KEY AND FOREIGN KEY ARE NOT
        # SOLO CONSTRAINTS AT THE TABLE LEVEL
        if constraints != None:
            if type(constraints) == list:
                for cstr in constraints:
                    if not isinstance(cstr,Constraint) and cstr not in Constraint.SOLO_CONSTRAINTS:
                        raise ValueError("{} is not a valid constraint".format(cstr))
            else:
                if not isinstance(cstr,Constraint) and cstr not in Constraint.SOLO_CONSTRAINTS:
                    raise ValueError("{} is not a valid constraint".format(constraint))
        
        # define the table
        self.name = name
        
        if type(fields) == list or fields == None:
            self.fields = fields
        else:
            self.fields = [fields]
            
        if type(constraints) == list or constraints == None:
            self.constraints = constraints
        else:
            self.constraints = [constraints]
            
    def create_cmd(self,if_not_exists=True,without_rowid=False):
        cmd = "CREATE TABLE "
        if if_not_exists:
            cmd += "IF NOT EXISTS " + self.name + " (\n"
        for i,fld in enumerate(self.fields):
            if i == len(self.fields)-1:
                cmd += "    " + fld.write() + "\n"
            else:
                cmd += "    " + fld.write() + ",\n"
        cmd += ")"
        if without_rowid:
            cmd += " WITHOUT_ROWID"    
        cmd += ";"
        
        return cmd
            
            
    
        
        
            
            