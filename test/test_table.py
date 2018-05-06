import pathmagic
import os
import unittest
from table import Field, FieldConstraint, Table, TableConstraint


class TableTestCase(unittest.TestCase):
    """
    DESCRIPTION
    """
    def test_field_constraint_saves_args_as_tuple(self):
        fc = FieldConstraint("DEFAULT", 5000.0)
        self.assertEqual(type(fc.args), tuple)

    def test_field_saves_constraints_as_list(self):
        f = Field("TestField", "BLOB", "NOT NULL")
        self.assertEqual(type(f.constraints), list)

    def test_invalid_field_constraint_list_raises_value_error(self):
        self.assertRaises(ValueError, Field, "TestField", "TEXT",
                          constraints=['PRIMARY KEY', 'NOT A CONSTRAINT'])

    def test_invalid_field_constraint_string_raises_value_error(self):
        self.assertRaises(ValueError, Field, "TestField", "TEXT", constraints="NOT A CONSTRAINT")

    def test_non_solo_field_constraint_without_arg_raises_value_error(self):
        self.assertRaises(ValueError, FieldConstraint, "DEFAULT")

    def test_table_constraint_with_no_args_raises_value_error(self):
        self.assertRaises(ValueError, TableConstraint, "DEFAULT")

    def test_write_check_field_constraint_formatting(self):
        fc = FieldConstraint("check", "SALARY > 0")
        actual = fc.write()
        expected = "CHECK(SALARY > 0)"
        self.assertEqual(actual, expected)

    def test_write_default_field_constraint_formatting(self):
        fc = FieldConstraint("default", 5000.)
        actual = fc.write()
        expected = "DEFAULT 5000.0"
        self.assertEqual(actual, expected)

    def test_write_field_with_constraint_formatting(self):
        fc = FieldConstraint("default", 5000.)
        f = Field("TestField", "text", fc)
        actual = f.write()
        expected = "TestField TEXT " + fc.write()
        self.assertEqual(actual, expected)

    def test_write_solo_field_constraint_formatting(self):
        fc = FieldConstraint("NOT NULL")
        actual = fc.write()
        expected = "NOT NULL"
        self.assertEqual(actual, expected)


